import xenarix as xen
import xenarix.sample as xen_s
import xenarix.results as xen_r

xen.set_repository('c:\\xenarix')

set_name = 'set1'
scenSet = xen.ScenarioSet(set_name=set_name)

scen_id = 'scen1'
result_id = 'res1'
scen1 = xen.Scenario(scen_id=scen_id, result_id=result_id)

scen1.general.scenario_num = 30
scen1.general.maxyear = 5

# make variable
kospi2_v = xen.ValueVariable('kospi2_v')
kospi2_v.value = 259

scen1.add_variable(kospi2_v)

gbmconst1 = xen_s.gbmconst('kospi200')
gbmconst1.x0 = kospi2_v
scen1.add_model(gbmconst1)

scen1.refresh_corr()

# variable shock
shock1 = xen.VariableShock('shock1')
# shock_variable : target,
shock1.add_shock_item(target_variable=kospi2_v, type='add', value=10)
#shock1.add_shock_item(target_variable=kospi2_v, type='mul', value=1.1)

scen1.add_shock(shock1)

scenSet.add_scenario(scen1)
scenSet.generate()

res = xen_r.ResultObj(set_name, scen_id, result_id)

print res.models['KOSPI200_NAN_BASE'].x0()
print res.models['KOSPI200_NAN_SHOCK1'].x0()