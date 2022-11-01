set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"
# PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
PATH_DIFF_VERSION="tests_unit/tests_diff_version"

# RDP 6
echo '----========RDP6 tests========----'
pip list
pip install th2-grpc-data-provider==1.1.0 -U -q
pytest tests/tests_unit -n auto --ignore tests/${PATH_DIFF_VERSION}/tests_v5


# RDP 5
echo '----========RDP5 tests========----'
pip list
pip install th2-grpc-data-provider==0.1.6 -U -q
pytest tests/tests_unit -n auto --ignore tests/${PATH_DIFF_VERSION}/tests_v6

