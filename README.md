Xenarix(Beta) : Economic Scenario Generator
==========================

![image](https://img.shields.io/badge/Platform-Windows-Green.svg)
![image](https://img.shields.io/pypi/pyversions/requests.svg)

Xenarix is a economic scenario generator(ESG) for financial analysis. Now is Beta Release version and Support only for Windows.

Feature Support
---------------

Functionalty :

-   Repository Setting
-   Multi-Thread Generating
-   TimeGrid Setting
-   Random Number Easy Change
-   Moment-Matching Random
-   Sobol Sequence Integrated

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

```
import xenarix as xen
import xenarix.sample as sample
import xenarix.results as xen_r

# default repository is sub-directory of your_working_directory
# ( [your_working_directory]/repository )
# xen.set_repository('c:\repository')

# scenario set
scenSetID = 'set1'
scenSet = xen.ScenarioSet(scenSetID)

# scenarioID , reusltID
scenID = 'scen1'
resultID = 'res1'
scen1 = xen.Scenario(scenID, resultID)

# generation setting (eq.)
scen1.general.scenario_num = 30
scen1.general.maxyear = 3

# model add
scen1.add_model(sample.gbm('kospi200'))
scen1.add_model(sample.gbmconst('kospi'))
scen1.add_model(sample.hw1f('irskrw'))

# set identity correlation
scen1.refresh_corr()

scenSet.add_scenario(scen1)

scenSet.generate()

# get result from current repository
result = xen_r.ResultObj(scenSetID, scenID, resultID)

print result.timegrid # pandas table shape(t_count, (INDEX, DATE, T, DT))

# select using scen_count
multipath = result.get_multipath(scen_count=1)
print (multipath) # pandas table shape(t_count, model_count)

# select using model_count
modelpath = result.get_modelpath(model_count=2)
print (modelpath) # ndarray : shape(scenarioNum, t_count)




```

License
-------

Xenarix(non-commercial version) is free for non-commercial purposes. 
This is licensed under the terms of the Montrix Non-Commercial License(see the file LICENSE).

Please contact us for the commercial purpose.

If you're interested in other financial application, visit [Montrix](http://www.montrix.co.kr)