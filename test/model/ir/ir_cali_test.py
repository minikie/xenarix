# coding=euc-kr
import bk1f_test
import cir1f_test
import cir1fext_test
import hw1f_test
import g2ext_test
import vasicek_test


bk1f_test.test(bk1f_test.get_test_model())
cir1f_test.test(cir1f_test.get_test_model())
cir1fext_test.test(cir1fext_test.get_test_model())
hw1f_test.test(hw1f_test.get_test_model())
g2ext_test.test(g2ext_test.get_test_model())
vasicek_test.test(vasicek_test.get_test_model())
