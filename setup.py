from setuptools import setup, find_packages

# requirements  = open("requirements.txt", "r")
# x = requirements.readlines()
# requirements .close()

version = '0.1.12'
#'SomePackage>=1.0.4'
#install_requires = [v.replace("\n", "") for v in x]

install_requires = ['numpy>=1.14.5',
                    'matplotlib>=2.2.2',
                    'pandas>=0.23.3',
                    'enum>=0.4.7']

setup(
    name             = 'xenarix',
    version          = version,
    description      = 'python library for xenarix',
    license          ='Montrix Non-Commercial License',
    author           = 'montrix',
    author_email     = 'master@montrix.co.kr',
    url              = 'http://www.montrix.co.kr/xenarix',
    install_requires = install_requires,
    packages         = find_packages(exclude = ['test']),
    keywords         = ['scenario', 'finance'],
    # python_requires  = '>=2.7',
    package_data     = {
        'xenarix': ['xenarix_engine.exe'],
    },
    zip_safe=False,
    classifiers      = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)