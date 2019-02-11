import xenarix as xen
import xenarix.sample as xen_s
import xenarix.results as xen_r

# default repository : [your_working_directory]\repository
xen.set_repository('c:\\xenarix')

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
    print t  # Pandas(INDEX=1L, DATE='2025-08-10', T=9.936986301369863, DT=0.002739726027396)

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