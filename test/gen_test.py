# coding=utf-8
import xenarix as xen
from xenarix import martingale as mart

xen.set_repository('C:\\Users\\09928829\\Source\\Workspaces\\InsuranceHedgeProject\\InsruranceHedge_sln\\Project\\Scenario\\xenarixPy\\test_repository')

set_name = 'setname_1'
scen_id = 'testallmodel_1'
result_id = 'testresult_1'

set1 = xen.ScenarioSet(set_name)

scen1 = xen.Scenario(scen_id, result_id)

scen1.general.scenario_num = 30



# bk1f = scen.BK1F('bk1f_test')
# bk1f.sections["FITTING_CURVE_TENOR"] = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
# bk1f.sections["FITTING_CURVE_VALUE"] = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]
# bk1f.sections["PARA_ALPHA_TENOR"] = ['36M']
# bk1f.sections["PARA_SIGMA_TENOR"] = ['12M', '24M', '36M']
# bk1f.sections["PARA_ALPHA_VALUE"] = [0.1]
# bk1f.sections["PARA_SIGMA_VALUE"] = [0.01, 0.01, 0.01]
# scen1.add_model(bk1f)
#
# cir1f = scen.CIR1F('cir1f_test')
# cir1f.sections["R0"] = 0.03
# cir1f.sections["PARA_ALPHA"] = 0.1
# cir1f.sections["PARA_LONGTERM"] = 0.1
# cir1f.sections["PARA_SIGMA"] = 0.01
# cir1f.sections["PARA_ALPHA_FIX"] = False
# cir1f.sections["PARA_LONGTERM_FIX"] = False
# cir1f.sections["PARA_SIGMA_FIX"] = False
# scen1.add_model(cir1f)

hw1f = xen.HullWhite1F('hw1f_test')
hw1f.fitting_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
hw1f.fitting_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]
hw1f.alpha_curve.tenor = ['36M']
hw1f.alpha_curve.value = [0.1]
hw1f.sigma_curve.tenor = ['36M']
hw1f.sigma_curve.value = [0.01]

scen1.add_model(hw1f)

fx1 = xen.GarmanKohlhagen('fx1')
fx1.dom_rf_curve.tenor = ['10Y']
fx1.dom_rf_curve.value = [0.02]
fx1.for_rf_curve.tenor = ['10Y']
fx1.for_rf_curve.value = [0.01]
fx1.sigma_curve.tenor= ['10Y']
fx1.sigma_curve.value = [0.3]

scen1.add_model(fx1)

scen1.refresh_corr()

set1.add_scenario(scen1)

set1.save()
# set1.generate()

mart.test_scenario_validation(scen1)

#scen_results = results.xeResultList(set1.set_name, scen_id, result_id)
#print(scen_results)

#scen1.save_as(set_name)
#scen1.generate()