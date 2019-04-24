import xenarix as xen
import xenarix.sample as xen_s
import xenarix.results as xen_r
import xenarix.viewer as xen_v
import xenarix.calculations as xen_c
import unittest, sys, datetime

def build_test_scen_set():
    test_scen_set = xen.ScenarioSet('test_scen_set')

    scen_num = 1000
    maxyear = 3
    moment_match = False
    rnd_seed = 10
    rnd_skip = 4096 * 2
    test_model = xen_s.gbm('test_gbm')
    calc_uncon_expectation = xen_c.UnconditionalExpectation()
    test_model.add_calc(calc_uncon_expectation)

    # for crude
    rnd_crude_subtype_list = [xen.RndSubType.MersenneTwister,
                          xen.RndSubType.Knuth,
                          xen.RndSubType.Lecuyer,
                          xen.RndSubType.Ranlux3,
                          xen.RndSubType.Ranlux4]

    for rnd_subtype in rnd_crude_subtype_list:
        scen = xen.Scenario('scen1', rnd_subtype + '_result')
        scen.general.scenario_num = scen_num
        scen.general.maxyear = maxyear
        scen.general.rnd_type = xen.RndType.Crude
        scen.general.rnd_subtype = rnd_subtype
        scen.general.rnd_seed = rnd_seed
        scen.general.rnd_skip  = rnd_skip
        scen.general.moment_match = moment_match
        scen.add_model(test_model)
        test_scen_set.add_scenario(scen)

    # for sobol
    rnd_sobol_subtype_list = [xen.RndSubType.Jaeckel,
                              xen.RndSubType.SobolLevitan,
                              xen.RndSubType.SobolLevitanLemieux,
                              xen.RndSubType.JoeKuoD5,
                              xen.RndSubType.JoeKuoD6,
                              xen.RndSubType.JoeKuoD7,
                              xen.RndSubType.Kuo,
                              xen.RndSubType.Kuo2,
                              xen.RndSubType.Kuo3]

    for rnd_subtype in rnd_sobol_subtype_list:
        scen = xen.Scenario('scen1', rnd_subtype + '_result')
        scen.general.scenario_num = scen_num
        scen.general.maxyear = maxyear
        scen.general.rnd_type = xen.RndType.Sobol
        scen.general.rnd_subtype = rnd_subtype
        scen.general.rnd_seed = rnd_seed
        scen.general.rnd_skip  = rnd_skip
        scen.general.moment_match = moment_match
        scen.add_model(test_model)
        test_scen_set.add_scenario(scen)

    # for Halton
    scen = xen.Scenario('scen1', xen_r.RndType.Halton + '_result')
    scen.general.scenario_num = scen_num
    scen.general.maxyear = maxyear
    scen.general.rnd_type = xen.RndType.Halton
    scen.general.moment_match = moment_match
    scen.general.rnd_seed = rnd_seed
    scen.general.rnd_skip = rnd_skip
    scen.add_model(test_model)
    test_scen_set.add_scenario(scen)

    # for Faure
    scen = xen.Scenario('scen1', xen_r.RndType.Faure + '_result')
    scen.general.scenario_num = scen_num
    scen.general.maxyear = maxyear
    scen.general.rnd_type = xen.RndType.Faure
    scen.general.moment_match = moment_match
    scen.general.rnd_seed = rnd_seed
    scen.general.rnd_skip = rnd_skip
    scen.add_model(test_model)
    test_scen_set.add_scenario(scen)

    return test_scen_set


if __name__ == '__main__':
    sys.argv.append('-v')

    test_scen_set = build_test_scen_set()
    test_scen_set.generate()
    result_obj_list = test_scen_set.get_result_obj_list()

    result_model = result_obj_list[0].get_resultModel_by_index(0)

    analytic = result_model.analytic()

    print(analytic)

    for result_obj in result_obj_list:
        result_model = result_obj.get_resultModel_by_index(0)
        #print(result_obj.result_name + ' : ' + result_model.name)
        print(result_obj.result_name)
        print(result_model.average())

    xen_v.plot_all(test_scen_set)
