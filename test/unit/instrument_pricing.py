# coding=utf-8
import xenarix as xen
import xenarix.sample as xen_s
import xenarix.results as xen_r
import xenarix.calculations as xen_c
import xenarix.instruments as xen_i
import xenarix.templatebuilder as xen_t
import xenarix.utilities as xen_u
import matplotlib.pyplot as plt
import unittest, sys, datetime

refdate = xen_u.datetime_to_datestr_yyyymmdd(datetime.datetime.now())

# gen을 해
gbm_model = xen_s.gbmconst('testgbm')
scen_set = xen_t.build_scenset_with_model(gbm_model, refdate)

# scen_set.generate()

res = scen_set.get_result_obj_list()

rm_list = res[0].get_resultModel_list()

rm1 = rm_list[0]
# rm2 = xen_r.ResultModel()

discount_curve = xen_i.FlatDiscountCurve(0.03)
maturity_date = xen_u.datetime_to_datestr_yyyymmdd(datetime.datetime.now())

# option = xen_i.IndexOption(type='call', strike=100, T=1.0)
option = xen_i.Kospi2_IndexOption(option_type='call', strike=100, maturity_date=maturity_date)
scenario_pricer = xen_i.ScenarioPricer(refdate=refdate, discount_curve=discount_curve)

print(scenario_pricer.price(instrument=option, rm_list=[rm1]))
# option.delta(up_rm_list=[rm1, rm2], dn_rm_list=[rm1, rm2])

x = gbm_model.x0
drift = gbm_model.rf - gbm_model.div
sigma = gbm_model.sigma
print(option.black_price(refdate, x, drift, sigma))

