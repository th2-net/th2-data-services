from pip._internal.operations.freeze import freeze
import pytest
from importlib_metadata import metadata, PackageNotFoundError


@pytest.fixture(scope="session")
def provider(pytestconfig):
    return pytestconfig.getoption("provider")


rdp = "th2-data-services-rdp"
lwdp = "th2-data-services-lwdp"


def test_provider_install(provider):
    if provider == 'rdp':
        assert metadata(rdp)
    elif provider == 'rdp5':
        assert metadata(rdp)['version'].startswith('5')
    elif provider == 'rdp6':
        assert metadata(rdp)['version'].startswith('6')
    elif provider == 'lwdp':
        assert metadata(lwdp)
    elif provider == 'lwdp1':
        assert metadata(lwdp)['version'].startswith('1')
    else:
        pytest.skip("Skipping Test")
