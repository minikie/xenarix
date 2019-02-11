# coding=utf-8
import xenarix as xen
import xenarix.results as xen_r
import xenarix.calculations as xen_c
import matplotlib.pyplot as plt


def shortrate(model, scenario_num=1000, maxyear=3, moment_match=False, frequency=xen.TimeGridFrequency.Day):
    if not isinstance(model, xen.Ir1FModel):
        raise Exception('Ir1FModel Type is needed')

    scenSetID = 'test_shortratecalc_set'
    scenID = 'test_shortratecalc_scen'
    resultID = 'test_shortratecalc_result'

    scenSet = xen.ScenarioSet(scenSetID)
    scen = xen.Scenario(scenID, resultID)

    scen.general.maxyear = maxyear
    scen.general.scenario_num = scenario_num
    scen.general.moment_match = moment_match
    scen.general.frequency = frequency

    model.clear_calc()
    # spot ----------------------------------------------
    calc_spot3M = xen_c.Spot('test_spot3m')
    calc_spot3M.maturity = '3M'
    model.add_calc(calc_spot3M)

    calc_spot6M = xen_c.Spot('test_spot6m')
    calc_spot6M.maturity = '6M'
    model.add_calc(calc_spot6M)

    calc_spot24M = xen_c.Spot('test_spot24m')
    calc_spot24M.maturity = '24M'
    model.add_calc(calc_spot24M)

    # forward ----------------------------------------------
    calc_forward_1M = xen_c.Forward('test_forward1m')
    calc_forward_1M.maturity = '1M'
    model.add_calc(calc_forward_1M)

    calc_forward_1Y_1M = xen_c.Forward('test_forward1y_1m')
    calc_forward_1Y_1M.forward_peoriod = '1Y'
    calc_forward_1Y_1M.maturity = '1M'
    model.add_calc(calc_forward_1Y_1M)

    calc_forward_1Y = xen_c.Forward('test_forward1y')
    calc_forward_1Y.maturity = '1Y'
    model.add_calc(calc_forward_1Y)

    calc_forward_1Y_1Y = xen_c.Forward('test_forward1y_1y')
    calc_forward_1Y_1Y.forward_peoriod = '1Y'
    calc_forward_1Y_1Y.maturity = '1Y'
    model.add_calc(calc_forward_1Y_1Y)

    # calc_cmt = xen_c.CMT('test_cmt')
    # model.add_calc(calc_cmt)
    #
    # calc_zerobond = xen_c.ZeroBond('test_zb')
    # model.add_calc(calc_zerobond)

    scen.add_model(model)
    scenSet.add_scenario(scen)

    scenSet.generate()

    res = xen_r.ResultObj(scenSetID, scenID, resultID)

    shortrate = res.get_resultModel(model=model)
    rm_calc_spot3M = res.get_resultModel(model=model, calc=calc_spot3M)
    rm_calc_spot6M = res.get_resultModel(model=model, calc=calc_spot6M)
    rm_calc_spot24M = res.get_resultModel(model=model, calc=calc_spot24M)

    # rm_calc_ = res.get_resultModel(model=model, calc=calc_zerobond)
    # rm_calc_cmt = res.get_resultModel(model=model, calc=calc_cmt)
    # rm_calc_zerobond = res.get_resultModel(model=model, calc=calc_zerobond)

    # plt.plot(shortrate_aver)
    # plt.plot(shortrate_uncon_expectation[0])
    plt.figure(1)
    plt.plot(res.timegrid.data['T'], shortrate.average(), label='shor_aver')
    plt.plot(res.timegrid.data['T'], rm_calc_spot3M.average(), label='spot_3m')
    plt.plot(res.timegrid.data['T'], rm_calc_spot6M.average(), label='spot_6m')
    plt.plot(res.timegrid.data['T'], rm_calc_spot24M.average(), label='spot_24m')
    plt.title('short_aver vs cmt_aver vs zerobond_aver')
    plt.xlabel('time (year)')
    plt.ylabel('rate (%)')

    plt.show()

# max diff position : 15 ( 1.73 Y )
# max diff value : 0.8 ( 0.1 % )
def equity(model, scenario_num=1000, maxyear=3, moment_match=False, frequency=xen.TimeGridFrequency.Day):
    if not isinstance(model, xen.Eq1FModel):
        raise Exception('Eq1FModel Type is needed')

    scenSetID = 'test_set'
    scenID = 'equity_test_scen'
    resultID = 'equity_test_result'

    scenSet = xen.ScenarioSet(scenSetID)
    scen = xen.Scenario(scenID, resultID)

    scen.general.maxyear = maxyear
    scen.general.scenario_num = scenario_num
    scen.general.moment_match = moment_match
    scen.general.frequency = frequency

    # setting additional calculation for martinagle test
    model.clear_calc()
    calc_randomZ = xen_c.RandomZ()
    model.add_calc(calc_randomZ)
    calc_uncon_expectation = xen_c.UnconditionalExpectation()
    model.add_calc(calc_uncon_expectation)

    scen.add_model(model)
    scenSet.add_scenario(scen)

    scenSet.generate()

    res = xen_r.ResultObj(scenSetID, scenID, resultID)

    equity = res.get_resultModel(model=model)
    equity_uncon_expectation = res.get_resultModel(model=model, calc=calc_uncon_expectation)

    rnd_z = res.get_resultModel(model=model, calc=calc_randomZ)

    plt.figure(1)
    plt.plot(res.timegrid.data['T'], equity.average(), label='equity_aver')
    plt.plot(res.timegrid.data['T'], equity_uncon_expectation.data[0], label='equity_analytic')
    plt.title('equity_aver vs equity_analytic')
    plt.xlabel('time (year)')
    plt.ylabel('value')
    plt.legend()

    plt.figure(2)
    plt.title('rand_z')
    plt.plot(rnd_z.average())
    plt.show()