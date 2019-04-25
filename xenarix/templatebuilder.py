# coding=utf-8
import xenarix as xen
import xenarix.sample as xen_s
import xenarix.results as xen_r
import xenarix.calculations as xen_c
import xenarix.instruments as xen_i
import xenarix.utilities as xen_u
import matplotlib.pyplot as plt
import unittest, sys, datetime


def build_scenset_with_model(model,
                             refdate=None,
                             set_name='set_name1',
                             scen_name='scen_name1',
                             result_name='result_name1'):

    scen_set = xen.ScenarioSet(set_name)
    scen1 = xen.Scenario(scen_name, result_name)
    _refdate = refdate

    if refdate is None:
        _refdate = xen_u.datetime_to_datestr_yyyymmdd(datetime.datetime.now())

    scen1.general.reference_date = _refdate

    # model type check
    if type(model) is list:
        for m in model:
            scen1.add_model(m)

        scen1.refresh_corr()
    else:
        scen1.add_model(model)

    scen_set.add_scenario(scen1)

    return scen_set

