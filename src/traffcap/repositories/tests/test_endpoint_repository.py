import pytest
from traffcap.repositories import EndpointRepository
from alchemy_mock.mocking import AlchemyMagicMock
"""
Tests for the endpoint repository
"""


class TestEndpointRepository:
    @pytest.mark.asyncio
    async def test_it_returns_one_endpoint_by_id(self, mocker):
        """
        Mock the Repository.session() to return the UnifiedAlchemyMagicMock
        TODO: Mock the sqlalchemy async session somehow
        """
        mocker.patch(
            "traffcap.repositories.Repository.session.__aenter__",
            return_value=AlchemyMagicMock()
        )
        results = await EndpointRepository.get_endpoint_by_id(1)

        assert results is not None
