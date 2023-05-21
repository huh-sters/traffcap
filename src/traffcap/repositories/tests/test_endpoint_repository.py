import pytest
from unittest import mock
from traffcap.repositories import EndpointRepository
from mock_alchemy.mocking import UnifiedAlchemyMagicMock
from traffcap.model import Endpoint
"""
Tests for the endpoint repository
"""


class TestEndpointRepository:
    @pytest.mark.asyncio
    async def test_it_returns_all_endpoints(self):
        """
        Mock the Repository.session() to return the UnifiedAlchemyMagicMock
        TODO: Mock the sqlalchemy async session somehow
        """
        mock_session = UnifiedAlchemyMagicMock(
            data=[(
                [mock.call.query(Endpoint)],
                [
                    Endpoint(id=1, code="abc123"),
                    Endpoint(id=2, code="abc456"),
                    Endpoint(id=3, code="abc789"),
                    Endpoint(id=4, code="abc012"),
                    Endpoint(id=5, code="abc345"),
                    Endpoint(id=6, code="abc678"),
                    Endpoint(id=7, code="abc901"),
                    Endpoint(id=8, code="abc234"),
                ]
            )]
        )
        results = await EndpointRepository.get_all_endpoints(session=mock_session)

        assert results is not None
