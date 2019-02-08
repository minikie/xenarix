# coding=utf-8
import xenarix as xen
import xenarix.test.martinagle as xen_mt
import xenarix.sample as xen_s

xen.set_repository('c:\\xenarix')

# hw1f = xen_s.hw1f('test_hw1')
#
# xen_t.shortrate(hw1f, scenario_num=1000, maxyear=5, moment_match=False, frequency=xen.TimeGridFrequency.Month)

# gbm = xen_s.gbm('test_gbm')
#
# xen_t.equity(gbm, scenario_num=1000, maxyear=5, moment_match=True, frequency=xen.TimeGridFrequency.Month)

gbmconst = xen_s.gbmconst('test_gbmconst')

xen_mt.equity(gbmconst, scenario_num=10000, maxyear=5, moment_match=True, frequency=xen.TimeGridFrequency.Month)