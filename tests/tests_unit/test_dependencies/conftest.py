def pytest_addoption(parser):
    parser.addoption("--provider", action="store", default="rdp")
