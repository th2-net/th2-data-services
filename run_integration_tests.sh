
PATH_DIFF_VERSION="tests_integration/tests_diff_version"

# RDP 6
echo '----========RDP6 tests========----'
pip install mypy-protobuf==2.5 th2-grpc-common==3.4.0 th2-grpc-data-provider==1.1.0 -U -q
pip list
python3 -m pytest tests/tests_integration -n 8 --ignore tests/${PATH_DIFF_VERSION}/tests_v5

# RDP 5
echo '----========RDP5 tests========----'
pip install protobuf==3.20.3 mypy-protobuf==3.2.0 th2-grpc-common==3.11.1 th2-grpc-data-provider==0.1.6 -U -q
pip list
python3 -m pytest tests/tests_integration -n 8 --ignore tests/${PATH_DIFF_VERSION}/tests_v6