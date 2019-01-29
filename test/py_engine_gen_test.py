# coding=euc-kr
import xenarix as xen

xen.set_repository('C:\\Users\\09928829\\Source\\Workspaces\\InsuranceHedgeProject\\InsruranceHedge_sln\\Project\\Scenario\\xenarixPy\\test_repository')

scen_id = 'testallmodel_2'
result_id = 'testresult_1'
set_name = 'setname_1'

set1 = xen.ScenarioSet(set_name)

scen1 = xen.Scenario(scen_id, result_id)

scen1.general.scenario_num = 30

hw1f = xen.HullWhite1F('hw1f_test')
hw1f.fitting_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
hw1f.fitting_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]
hw1f.alpha_curve.tenor = ['36M']
hw1f.alpha_curve.value = [0.1]
hw1f.sigma_curve.tenor = ['36M']
hw1f.sigma_curve.value = [0.01]

scen1.add_model(hw1f)

scen1.refresh_corr()

set1.add_scenario(scen1)

set1.generate()

#set1.save()

# set1.generate()
#scen_results = results.xeResultList(set1.set_name, scen_id, result_id)
#print(scen_results)

#scen1.save_as(set_name)
#scen1.generate()