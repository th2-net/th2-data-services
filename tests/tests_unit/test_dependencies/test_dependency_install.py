from pip._internal.operations.freeze import freeze
import pytest
from importlib_metadata import metadata, PackageNotFoundError


@pytest.fixture(scope="session")
def provider(pytestconfig):
    return pytestconfig.getoption("provider")


packages = {}
for pkg in freeze():
    k, v = pkg.split("==")
    packages[k] = v

rdp = "th2-data-services-rdp"
lwdp = "th2-data-services-lwdp"


def test_rdp_install(provider):
    if provider == 'rdp':
        if rdp in packages:
            assert metadata(rdp)
            print("RDP Package Exists")
        else:
            with pytest.raises(PackageNotFoundError):
                print("RDP Package Doesn't Exist")
                assert metadata(rdp)


def test_rdp_v5_install(provider):
    if provider == 'rdp5':
        if rdp in packages:
            assert metadata(rdp)
            assert metadata(rdp)['version'].startswith('5')
            print("RDPv5 Package Exists")
        else:
            with pytest.raises(PackageNotFoundError):
                print("RDPv5 Package Doesn't Exist")
                assert metadata(rdp)


def test_rdp_v6_install(provider):
    if provider == 'rdp6':
        if rdp in packages:
            assert metadata(rdp)
            assert metadata(rdp)['version'].startswith('6')
            print("RDPv6 Package Exists")
        else:
            with pytest.raises(PackageNotFoundError):
                print("RDPv6 Package Doesn't Exist")
                assert metadata(rdp)


def test_lwdp_install(provider):
    if provider == 'lwdp':
        if lwdp in packages:
            assert metadata(lwdp)
            print("LwDP Package Exists")
        else:
            with pytest.raises(PackageNotFoundError):
                print("LwDP Package Doesn't Exist")
                assert metadata(lwdp)


def test_lwdp_v1_install(provider):
    if provider == 'lwdp1':
        if lwdp in packages:
            assert metadata(lwdp)
            assert metadata(lwdp)['version'].startswith('1')
            print("LwDPv1 Package Exists")
        else:
            with pytest.raises(PackageNotFoundError):
                print("LwDPv1 Package Doesn't Exist")
                assert metadata(lwdp)
