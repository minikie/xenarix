import xenarix as xen
import xenarix.sample as xen_s

xen.set_repository('c:\\xenarix')

set_name = 'set1'
scenSet = xen.ScenarioSet(set_name=set_name)

scen_id = 'scen1'
result_id = 'res1'
scen1 = xen.Scenario(scen_id=scen_id, result_id=result_id)

scen1.general.scenario_num = 30
scen1.general.maxyear = 5

gbm1 = xen_s.gbmconst('kospi200')
gbm2 = xen_s.gbmconst('kospi200_2')

scen1.add_model(gbm1)
scen1.add_model(gbm2)

scenSet.add_scenario(scen1)

scen1.refresh_corr()
scen1.set_corr(gbm1, gbm2, 0.0)

#print scen1.dump()

scenSet.generate()

