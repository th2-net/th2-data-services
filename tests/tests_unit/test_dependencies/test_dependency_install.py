from pip._internal.operations.freeze import freeze
import pytest
from importlib_metadata import metadata, PackageNotFoundError


@pytest.fixture(scope="session")
def provider(pytestconfig):
    return pytestconfig.getoption("provider").lower()


rdp = "th2-data-services-rdp"
lwdp = "th2-data-services-lwdp"


def test_provider_install(provider):
    if provider in ['rdp', 'rdp-dev']:
        assert metadata(rdp)
    elif provider in ['rdp5', 'rdp5-dev']:
        assert metadata(rdp)['version'].startswith('5')
    elif provider in ['rdp6', 'rdp6-dev']:
        assert metadata(rdp)['version'].startswith('6')
    elif provider in ['lwdp', 'lwdp-dev']:
        assert metadata(lwdp)
    elif provider in ['lwdp1', 'lwdp1-dev']:
        assert metadata(lwdp)['version'].startswith('1')
    else:
        pytest.skip("Skipping Test")
