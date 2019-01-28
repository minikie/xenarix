# coding=euc-kr
import xenarix as scen
from xenarix import martingale as mart
import test.model.all_test as test_model

scen_id = 'testallmodel_1'
result_id = 'testresult_1'
set_name = 'setname_1'

set1 = scen.ScenarioSet(set_name)

scen1 = scen.Scenario(scen_id, result_id)

scen1.general.scenario_num = 200
scen1.general.maxyear = 30
scen1.general.rnd_seed = 16
scen1.general.frequency = 'MONTH'
scen1.general.rnd_type = 'SOBOL'

gbm = test_model.gbm.get_test_model('gbm_test')
gbmconst = test_model.gbmconst.get_test_model('gbmconst_test')
gk = test_model.gk.get_test_model('gk_test')
hw1f = test_model.hw1f.get_test_model('hw1f_test')
bk1f = test_model.bk1f.get_test_model('bk1f_test')
cir1f = test_model.cir1f.get_test_model('cir1f_test')
cir1fext = test_model.cir1fext.get_test_model('cir1fext_test')
vasicek = test_model.vasicek.get_test_model('vasicek_test')
heston = test_model.heston.get_test_model('heston_test')

# scen1.add_model(gbmconst) #
# scen1.add_model(gbm) # const에 비해 vol때매 좀 느림
# scen1.add_model(gk)
scen1.add_model(hw1f)
# scen1.add_model(bk1f)
# scen1.add_model(cir1f)
# scen1.add_model(cir1fext)
# scen1.add_model(vasicek)
# scen1.add_model(heston)

scen1.refresh_corr()

set1.add_scenario(scen1)

set1.save()
# set1.generate()

mart.test_scenario_validation(scen1)

#scen_results = results.xeResultList(set1.set_name, scen_id, result_id)
#print(scen_results)

#scen1.save_as(set_name)
#scen1.generate()