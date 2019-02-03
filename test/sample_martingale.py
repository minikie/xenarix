import xenarix as xen
import xenarix.test as xen_t
import xenarix.sample as xen_s

hw1f = xen_s.hw1f('test_hw1')

xen_t.shortrate(hw1f, scenario_num=1000, maxyear=15, moment_match=False, frequency=xen.TimeGridFrequency.Month)

gbm = xen_s.gbm('test_gbm')

xen_t.equity(gbm, scenario_num=1000, maxyear=15, moment_match=True, frequency=xen.TimeGridFrequency.Month)