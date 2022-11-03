
PATH_DIFF_VERSION="tests_unit/tests_diff_version"

# RDP 6
echo '----========RDP6 tests========----'
pip install th2-grpc-data-provider==1.1.0 -U -q
#pin install th2-grpc-common==3.11.1
pip list
pytest tests/tests_unit -n auto --ignore tests/${PATH_DIFF_VERSION}/tests_v5


# RDP 5
echo '----========RDP5 tests========----'
pip install th2-grpc-data-provider==0.1.6 -U -q
pip install mypy-protobuf==2.5
#pin install th2-grpc-common==3.11.1
pip list
pytest tests/tests_unit -n auto --ignore tests/${PATH_DIFF_VERSION}/tests_v6

