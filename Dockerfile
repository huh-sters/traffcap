FROM python:3.8.18-alpine AS base_image

ENV PATH=/root/.local/bin:$PATH \
    TRAFFCAP_REQUESTS_PREFIX="r" \
    TRAFFCAP_DB_USER="" \
    TRAFFCAP_DB_PASSWORD="" \
    TRAFFCAP_DB_HOST="" \
    TRAFFCAP_DB_NAME="/data/traffcap.db" \
    TRAFFCAP_DB_DRIVER="sqlite" \
    TRAFFCAP_SERVER_URL="localhost:9669" \
    PYTHONPATH="src/traffcap"

EXPOSE 9669

RUN apk --no-cache add curl nodejs npm && \
    mkdir /traffcap && \
    mkdir /data

COPY . /traffcap

WORKDIR /traffcap

# Install Python dependencies
RUN curl -sSL https://pdm.fming.dev/install-pdm.py | python3 - && \
    pdm install --production

# Build frontend
RUN cd src/traffcap/spa && \
    npm install && \
    npm run build

WORKDIR /traffcap/src

VOLUME /data

CMD pdm run server
