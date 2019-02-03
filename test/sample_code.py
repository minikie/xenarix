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
scen1.general.scenario_num = 100
scen1.general.maxyear = 10

# model add
scen1.add_model(sample.gbm('kospi200'))
scen1.add_model(sample.gbmconst('kospi'))
#scen1.add_model(sample.hw1f('irskrw'))

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
modelpath = result.get_modelpath(model_count=1)
print (modelpath) # ndarray : shape(scenarioNum, t_count)
