from sys import argv
from pip._internal.operations.freeze import freeze

packages = {}
for pkg in freeze():
    k, v = pkg.split("==")
    packages[k] = v

provider = argv[1] if len(argv) > 1 else None

rdp = "th2-data-services-rdp"
lwdp = "th2-data-services-lwdp"

if provider:
    if provider == 'rdp':
        print(f"Installing --> {provider=}")
        import th2_data_services_rdp
    elif provider == 'rdp5':
        print(f"Installing --> {provider=}")
        import th2_data_services_rdp
        assert packages[rdp][0] == '5'
    elif provider == 'rdp6':
        print(f"Installing --> {provider=}")
        import th2_data_services_rdp
        assert packages[rdp][0] == '6'
    elif provider == 'lwdp':
        print(f"Installing --> {provider=}")
        import th2_data_services_lwdp
    elif provider == 'lwdp1':
        print(f"Installing --> {provider=}")
        import th2_data_services_lwdp
        assert packages[lwdp][0] == '1'
