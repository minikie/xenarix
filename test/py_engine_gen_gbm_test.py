# coding=euc-kr
import xenarix as xen

xen.set_repository('C:\\Users\\09928829\\Source\\Workspaces\\InsuranceHedgeProject\\InsruranceHedge_sln\\Project\\Scenario\\xenarixPy\\test_repository')

set_name = 'setname_1'
scen_id = 'testscen_1'
result_id = 'testresult_1'

set1 = xen.ScenarioSet(set_name)

scen1 = xen.Scenario(scen_id, result_id)

scen1.general.scenario_num = 30

gbm1 = xen.GBM('gbm1')
gbm1.rf_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
gbm1.rf_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]

gbm1.div_curve.tenor = ['15Y']
gbm1.div_curve.value = [ 0.005]

gbm1.sigma_curve.tenor = ['15Y']
gbm1.sigma_curve.value = [0.3]

gbm2 = xen.GBM('gbm2')
gbm2.rf_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
gbm2.rf_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]

gbm2.div_curve.tenor = ['15Y']
gbm2.div_curve.value = [ 0.005]

gbm2.sigma_curve.tenor = ['15Y']
gbm2.sigma_curve.value = [0.3]

scen1.add_model(gbm1)
scen1.add_model(gbm2)

scen1.refresh_corr()

set1.add_scenario(scen1)
set1.generate()
