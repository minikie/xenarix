# coding=euc-kr
import xenarix as scen
import martingale as mart
import test.model.all_test as test_model
import results

scen_id = 'testallmodel_1'
result_id = 'testresult_1'
set_name = 'setname_1'

set1 = scen.ScenarioSet(set_name)

scen1 = scen.Scenario(scen_id, result_id)

scen1.general.scenario_num = 30
scen1.general.maxyear = 50
scen1.general.frequency = 'MONTH'

hw1f = test_model.hw1f.get_test_model('hw1f_test')
bk1f = test_model.bk1f.get_test_model('bk1f_test')
cir1f = test_model.cir1f.get_test_model('cir1f_test')
vasicek = test_model.vasicek.get_test_model('vasicek_test')

scen1.add_model(hw1f)
scen1.add_model(bk1f)
scen1.add_model(cir1f)
scen1.add_model(vasicek)

scen1.refresh_corr()

set1.add_scenario(scen1)

set1.save()
# set1.generate()

mart.test_scenario_validation(scen1)

#scen_results = results.xeResultList(set1.set_name, scen_id, result_id)
#print(scen_results)

#scen1.save_as(set_name)
#scen1.generate()