FROM python:3.9.21-alpine AS base_image

ENV PATH=/root/.local/bin:$PATH \
    TRAFFCAP_REQUESTS_PREFIX="r" \
    TRAFFCAP_DB_USER="" \
    TRAFFCAP_DB_PASSWORD="" \
    TRAFFCAP_DB_HOST="" \
    TRAFFCAP_DB_NAME="/data/traffcap.db" \
    TRAFFCAP_DB_DRIVER="sqlite" \
    TRAFFCAP_SERVER_URL="localhost:9669" \
    PYTHONPATH="src/traffcap" \
    VITE_WS_API_URL="http://localhost:9669" \
    VITE_API_URL="http://localhost:9669" \
    BASE_URL="http://localhost:9669"

EXPOSE 9669

RUN apk --no-cache add curl nodejs npm && \
    mkdir /traffcap && \
    mkdir /data

COPY . /traffcap

WORKDIR /traffcap

# Install Python dependencies
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    uv sync --no-dev && \
    uv cache clean

# Build frontend
RUN cd src/traffcap/spa && \
    npm install && \
    npm run build && \
    rm -rf node_modules && \
    npm cache clean --force

WORKDIR /traffcap/src

VOLUME /data

CMD uv run ./server
