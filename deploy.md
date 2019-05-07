https://rampart81.github.io/post/python_package_publish/ 여기서 비슷하게 함
python 설치된 곳 scripts 디렉토리에 pip있음
거기서 pip install wheel 이랑 pip install setuptools  해야함
그러고 와서 python.exe setup.py bdist_wheel 하면 디렉토리 dist에 배포파일생김
그거 python -m pip install mxfbook-0.1.1-py2-none-any.whl 하면됨
버전은 알아서 올려서 다시 빌드하면 되고..

python setup.py bdist_wheel -> 배포파일 만들기

----------------------------------------------------------------
setup 을 실행하면, packages 에 python package 폴더가 들어가는데
일반 폴더는 안들어가고, __init__.py 있는 폴더만 들어감
확인하려면 lib\site-package\ 폴더에서 확인하면 들어간거 확인 가능 함.

------------------------------------------------

MEANIFEST.in 파일에 포함할 binary file 추가함.

--------------------------------------------

python setup_mxd.py sdist bdist -> 배포파일 만들기
python -m pip install mxd-0.1.0.tar.gz

-------------------------------------------
pypi에 올리는 방법
https://jwkcp.github.io/2018/03/11/how-to-deploy-to-pypi/
pypi upload는 twine을 깔고

test server -> twine upload --repository-url https://test.pypi.org/legacy/ dist/*
real server -> twine upload dist/*

pip install --index-url https://test.pypi.org/simple/ xenarix