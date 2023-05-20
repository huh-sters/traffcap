import pytest
from traffcap.repositories import EndpointRepository
"""
Tests for the endpoint repository
"""


class TestEndpointRepository:
    @pytest.mark.asyncio
    async def test_it_returns_one_endpoint_by_id(self):
        """
        Mock the Repository.session() to return the UnifiedAlchemyMagicMock
        """
        results = await EndpointRepository.get_endpoint_by_id(1)

        assert results is not None
