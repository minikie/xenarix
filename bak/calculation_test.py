# coding=utf-8
import xenarix as xen
import xenarix.test.calculation as xen_ct
import xenarix.sample as xen_s

xen.set_repository('c:\\xenarix')

hw1f = xen_s.hw1f('test_hw1')
xen_ct.shortrate(hw1f, scenario_num=200, maxyear=5, moment_match=False, frequency=xen.TimeGridFrequency.Month)
