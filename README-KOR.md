Xenarix(Beta) : 경제 시나리오 발생기
==========================

![image](https://img.shields.io/badge/Platform-Windows-Green.svg)
![image](https://img.shields.io/badge/Platform-Linux-Orange.svg)
![image](https://img.shields.io/pypi/pyversions/requests.svg)

[ENG Version](README.md)

Xenarix 는 금융 분석을 위한 경제 시나리오 발생기(ESG) 입니다. 

특징
---------------

기능 :

-   결과 저장소 설정
-   멀티스레드 지원
-   TimeGrid Setting
-   난수 변경 (메르센트위스터, 소볼)
-   적률일치법

Models : 

-   Geometric Brownian Motion ( Constant Paramter, Time-Varying Parameter )   
-   Hull-White 1 Factor
-   Vasicek 1 Factor
-   Cox-Ingersoll-Ross 1 Factor
-   Black-Karasinsky
-   Garman-Kohlhagen


실행가능 Python 버전 : 2.7 & 3.4–3.7

사용법
-----------

Xenarix 설치 방법 - 아래와 같은 명령어를 실행 :

``` {.sourceCode .bash}
$ pip install xenarix
```

시나리오 생성 예제 :

```python

import xenarix as xen
import xenarix.sample as xen_s
import xenarix.results as xen_r

# default repository : [your_working_directory]\repository
# xen.set_repository('c:\repository')

# scenario set
set_name = 'set1'
scenSet = xen.ScenarioSet(set_name=set_name)

# scenario
scen_id = 'scen1'
result_id = 'res1'
scen1 = xen.Scenario(scen_id=scen_id, result_id=result_id)

# generation setting
scen1.general.scenario_num = 100
scen1.general.maxyear = 10

# model add
scen1.add_model(xen_s.gbm('kospi200'))
scen1.add_model(xen_s.gbmconst('kospi'))
scen1.add_model(xen_s.hw1f('irskrw'))

# set identity correlation
scen1.refresh_corr()

scenSet.add_scenario(scen1)
scenSet.generate()

# get result from current repository
res = xen_r.ResultObj(set_name, scen_id, result_id)

# timegrid iter is pandas namedtuple
for t in res.timegrid:
    print t  # Pandas(INDEX=16L, DATE='2015-09-18', T=0.043835616438356005, DT=0.0027397260273970005)

# select using scen_count
multipath = res.get_multipath(scen_count=1)
print (multipath)  # pandas table shape(t_count, model_count)
#         IRSKRW       KOSPI    KOSPI200
# 0     0.014700  100.000000  100.000000
# 1     0.015064   98.939790  101.055454

# select using model_count
modelpath = res.get_modelpath(model_count=1)
print (modelpath)  # ndarray : shape(scenarioNum, t_count)
# [3654 rows x 3 columns]
# [100.          99.99079151  99.98158388 ...  86.98067194  86.98100591 86.98134017]
# [100.         101.05545434  99.98158388 ...  74.89920039  75.41241596 74.8997758 ]

```

Result Viwer
-----------
You can download Result Viewr [XenarixResultViewer](https://github.com/minikie/xenarix/releases/latest)
Download ResultViewer.Zip and Run Setup.exe 

![ScreenShot](/img/resultviewer.png?raw=true)

라이센스
-------

Xenarix(비상업용 버전)는 비상업 목적으로 사용 시 무료입니다. 
자세한 사항은 Montrix 비-상업용 라이센스파일(LICENSE)에 참조.

상업적으로 사용 시에는 연락 부탁드립니다. <master@montrix.co.kr>

당사는 금융 관련 솔루션 사업을 영위하고 있습니다. 홈페이지 : [Montrix](http://www.montrix.co.kr)
