import xenarix as xen

import test.model.eq.gbm_test as gbm
import test.model.eq.gbmconst_test as gbmconst
import test.model.eq.heston_test as heston

import test.model.fx.gk_test as gk

import test.model.ir.hw1f_test as hw1f
import test.model.ir.bk1f_test as bk1f
import test.model.ir.cir1f_test as cir1f
import test.model.ir.cir1fext_test as cir1fext
import test.model.ir.vasicek_test as vasicek

import test.model.etc.random_test as random_test
import test.model.etc.brownian_motion_test as brownian_motion_test

xen.set_repository('c:\\xenarix')

brownian_motion_test.do_test()


