
echo '----========unit tests========----'
pip list
python3 -m pytest tests/tests_unit -n auto --ignore tests/tests_unit/test_dependencies/
