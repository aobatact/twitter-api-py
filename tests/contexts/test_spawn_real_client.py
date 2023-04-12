import pytest

from tests.contexts.spawn_real_client import spawn_real_client
from twitter_api.error import NeverError, UnsupportedAuthenticationError


class TestSpawnRealClient:
    def test_spawn_real_client_is_success_when_permit(
        self,
        request: pytest.FixtureRequest,
    ):
        with spawn_real_client("real_oauth2_app_client", request, permit=True) as _:
            pass

    def test_spawn_real_client_is_failed_when_permit(
        self,
        request: pytest.FixtureRequest,
    ):
        with pytest.raises(NeverError):
            with spawn_real_client("real_oauth2_app_client", request, permit=True) as _:
                raise NeverError(None)  # type: ignore

    def test_spawn_real_client_is_success_when_non_permit(
        self,
        request: pytest.FixtureRequest,
    ):
        with pytest.raises(UnsupportedAuthenticationError):
            with spawn_real_client(
                "real_oauth2_app_client", request, permit=False
            ) as _:
                pass

    def test_spawn_real_client_is_failed_when_non_permit(
        self,
        request: pytest.FixtureRequest,
    ):
        with pytest.raises(NeverError):
            with spawn_real_client(
                "real_oauth2_app_client", request, permit=False
            ) as _:
                raise NeverError(None)  # type: ignore