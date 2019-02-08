# coding=euc-kr

from test import bk1f_test, test as cir1f_test, test as cir1fext_test, test as hw1f_test, test as vasicek_test, \
    test as gbm_test, test as gbmconst_test

# import gbmlocalvol_test
# import cev_test
# import cevconst_test
# import cevlocalvol_test

import xenarix as scen

scen1 = scen.Scenario()
scen1.general.sections["SCENARIO_NUM"] = 30

# ir
scen1.add_model(bk1f_test.get_test_model('bk1f_test'))
scen1.add_model(cir1f_test.get_test_model('cir1f_test'))
scen1.add_model(cir1fext_test.get_test_model('cir1fext_test'))
scen1.add_model(hw1f_test.get_test_model('hw1f_test'))
#scen1.add_model(g2ext_test.get_test_model('g2ext_test'))
scen1.add_model(vasicek_test.get_test_model('vasicek_test'))

# eq
scen1.add_model(gbm_test.get_test_model('gbm_test'))
scen1.add_model(gbmconst_test.get_test_model('gbmconst_test'))
#scen1.add_model(gbmlocalvol_test.get_test_model('gbmlocalvol_test'))
scen1.add_model(cev_test.get_test_model('cev_test'))
scen1.add_model(cevconst_test.get_test_model('cevconst_test'))
#scen1.add_model(cevlocalvol_test.get_test_model('cevlocalvol_test'))
#scen1.add_model(heston_test.get_test_model('heston_test'))

scen1.refresh_corr()

scen1.save_as('parallel_test')
scen1.generate('parallel_test', 'parallel_result')