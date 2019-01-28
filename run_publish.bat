del .\dist\* /q
python setup.py sdist bdist_wheel
c:\Python27\Scripts\twine.exe upload -u montrix --repository-url https://test.pypi.org/legacy/ dist/*