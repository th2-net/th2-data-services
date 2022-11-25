
echo '----========unit tests========----'
pip list
pytest tests/tests_unit -n auto --ignore tests/tests_unit/test_dependencies/
