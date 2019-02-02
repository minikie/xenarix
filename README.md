Xenarix : Economic Scenario Generator (Python)
==========================

[![image](https://img.shields.io/badge/Platform-Windows-Green.svg)](https://pypi.org/project/requests/)
[![image](https://img.shields.io/pypi/pyversions/requests.svg)](https://pypi.org/project/requests/)



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
import xenarix.result as xen_r

# default repository is sub-directory of your_working_directory
# ( [your_working_directory]/repository ) 
# xen.set_repository('c:\repository')

scenSetID='set1'
scenID='scen1'
resultID='res1'

xen.test_generate(scenSetID, scenID, resultID)

# get result from current repository
result = xen_r.ResultObj(scenSetID, scenID, resultID)

multipath = result.get_multipath(scen_count=0) # select using scen_count
modelpath = result.get_modelpath(model_count=0) # 



```

License
-------

Xenarix(non-commercial version) is free for non-commercial purposes. 
This is licensed under the terms of the Montrix Non-Commercial License(see the file LICENSE).

Please contact us for the commercial purpose.

If you're interested in other finacial application, visit [Montrix](http://www.montrix.co.kr)

About
------
This is a [QunatLib](https://www.quantlib.org) based Software.  