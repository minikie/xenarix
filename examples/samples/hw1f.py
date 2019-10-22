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
hw1f = xen_s.hw1f('irskrw')
scen1.add_model(hw1f)


scenSet.add_scenario(scen1)
scenSet.generate()

# get result from current repository
res = xen_r.ResultObj(set_name, scen_id, result_id)

# timegrid iter is pandas namedtuple
for t in res.timegrid:
    print(t)

# select using scen_count
multipath = res.get_multipath(scen_count=15)
print (multipath)

# select using model_count
modelpath = res.get_modelpath(model_count=0)
print (modelpath)
