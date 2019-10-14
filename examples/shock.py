import xenarix as xen
import xenarix.sample as xen_s
import xenarix.results as xen_r
import xenarix.viewer as xen_v

xen.set_repository('c:\\xenarix')

set_name = 'set1'
scenSet = xen.ScenarioSet(set_name=set_name)

scen_id = 'scen1'
result_id = 'res1'
scen1 = xen.Scenario(scen_id=scen_id, result_id=result_id)

scen1.general.scenario_num = 30
scen1.general.maxyear = 5

# make variable
kospi2_v = xen.ValueVariable('kospi2_v', 259)

scen1.add_variable(kospi2_v)

irskrw = xen.YieldCurveVariable('irskrw')
irskrw.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
irskrw.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]

kospi2_imvol = xen.VolCurveVariable('kospi2_imvol')
kospi2_imvol.tenor = ['1Y', '2Y', '3Y', '4Y', '5Y']
kospi2_imvol.value = [0.3, 0.3, 0.3, 0.3, 0.3]

scen1.add_variable(irskrw)
scen1.add_variable(kospi2_imvol)

gbm1 = xen_s.gbm('kospi200')
gbm1.x0 = kospi2_v
gbm1.rf_curve = irskrw
gbm1.div_curve = 0.01
gbm1.sigma_curve = kospi2_imvol

scen1.add_model(gbm1)

scen1.refresh_corr()

# value variable shock
#shock1 = xen.VariableShock('shock1')
# shock_variable : target,
#shock1.add_shock_item(target_variable=kospi2_v, type='add', value=-10)
#shock1.add_shock_item(target_variable=kospi2_v, type='mul', value=1.1)
#shock1.add_shock_item(target_variable=kospi2_v, type='custom', value=255)

#scen1.add_shock(shock1)

# curve variable shock
shock2 = xen.VariableShock('shock2')
# shock_variable : target,
#shock2.add_shock_item(target_variable=irskrw, type='add', value=0.01)
shock2.add_shock_item(target_variable=irskrw, type='add', value=[0.01, 0.01])
#shock2.add_shock_item(target_variable=irskrw, type='mul', value=1.1)
#shock2.add_shock_item(target_variable=irskrw, type='custom', value=[0.01])

shock2.add_shock_item(target_variable=kospi2_imvol, type='add', value=0.05)

scen1.add_shock(shock2)

scenSet.add_scenario(scen1)
scenSet.generate_test()

res = xen_r.ResultObj(set_name, scen_id, result_id)

print(res.res_models)

xen_v.plot_all(res)