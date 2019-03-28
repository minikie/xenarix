del .\dist\* /q
python setup.py sdist bdist_wheel
::python -m twine upload -u montrix --repository-url https://test.pypi.org/legacy/ dist/*
python -m twine upload -u montrix dist/*