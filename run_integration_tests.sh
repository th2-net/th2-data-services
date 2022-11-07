
PATH_DIFF_VERSION="tests_integration/tests_diff_version"

# RDP 6
pip install th2-grpc-data-provider==1.1.0 -U -q
pytest tests/tests_unit -n 8 --ignore tests/${PATH_DIFF_VERSION}/tests_v5


# RDP 5
pip install th2-grpc-data-provider==0.1.6 -U -q
pytest tests/tests_unit -n 8 --ignore tests/${PATH_DIFF_VERSION}/tests_v6

