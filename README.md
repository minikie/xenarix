Xenarix(Beta) : Economic Scenario Generator
==========================

![image](https://img.shields.io/badge/Platform-Windows-Green.svg)
![image](https://img.shields.io/pypi/pyversions/requests.svg)

[한글 버전](README-KOR.md)

Xenarix is a economic scenario generator(ESG) for financial analysis. Now is Beta Release version and Support only for Windows.
The Engine is developed by C++. 

Feature Support
---------------

Functionalty :

-   Repository Setting
-   Multi-Thread Generating
-   TimeGrid Setting
-   Random Number Change (Mersenne Twister, Sobol)
-   Moment-Matching Random

Models : 

-   Geometric Brownian Motion ( Constant Paramter, Time-Varying Parameter )   
-   Hull-White 1 Factor
-   Vasicek 1 Factor
-   Cox-Ingersoll-Ross 1 Factor
-   Black-Karasinsky
-   Garman-Kohlhagen


Requests officially supports Python 2.7 & 3.4–3.7

Quick start
-----------

To install Xenarix, simply use pip :

``` {.sourceCode .bash}
$ pip install xenarix
```

Sample Generation Script :

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

Result Viewer
-----------
You can download [ResultViwer](https://github.com/minikie/xenarix/releases/latest) For Windows 

Download ResultViewer.Zip and Run Setup.exe 

![ScreenShot](/img/resultviewer.png?raw=true)

License
-------

Xenarix(non-commercial version) is free for non-commercial purposes. 
This is licensed under the terms of the Montrix Non-Commercial License(see the file LICENSE).

Please contact us for the commercial purpose. <master@montrix.co.kr>

If you're interested in other financial application, visit [Montrix](http://www.montrix.co.kr)
