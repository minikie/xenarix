# coding=utf-8
import xenarix as xen
import xenarix.results as xen_r
import xenarix.calculations as xen_c
import matplotlib.pyplot as plt


def shortrate(model, scenario_num=1000, maxyear=3, moment_match=False, frequency=xen.TimeGridFrequency.Day):
    if not isinstance(model, xen.Ir1FModel):
        raise Exception('Ir1FModel Type is needed')

    scenSetID = 'test_set'
    scenID = 'test_scen'
    resultID = 'test_result'

    scenSet = xen.ScenarioSet(scenSetID)
    scen = xen.Scenario(scenID, resultID)

    scen.general.maxyear = maxyear
    scen.general.scenario_num = scenario_num
    scen.general.moment_match = moment_match
    scen.general.frequency = frequency.value

    # setting additional calculation for martinagle test
    model.clear_calc()
    calc_randomZ = xen_c.RandomZ()
    model.add_calc(calc_randomZ)
    calc_uncon_expectation = xen_c.UnconditionalExpectation()
    model.add_calc(calc_uncon_expectation)
    calc_mrk_discount = xen_c.FittingDiscount()
    model.add_calc(calc_mrk_discount)
    calc_model_discount = xen_c.ModelDiscount()
    model.add_calc(calc_model_discount)

    scen.add_model(model)
    scenSet.add_scenario(scen)

    scenSet.generate()

    res = xen_r.ResultObj(scenSetID, scenID, resultID)

    shortrate = res.get_resultModel(model=model)
    shortrate_uncon_expectation = res.get_resultModel(model=model, calc=calc_uncon_expectation)
    mrk_discount = res.get_resultModel(model=model, calc=calc_mrk_discount)
    model_discount = res.get_resultModel(model=model, calc=calc_model_discount)

    rnd_z = res.get_resultModel(model=model, calc=calc_randomZ)


    print(mrk_discount.data[0])

    # result_list['BASE_FITTINGDISCOUNT'].load(1, 1)
    #
    # shortrate_aver = result_list['BASE_nan'].averave()
    # shortrate = result_list['BASE_nan'].load()
    # shortrate_uncon_expectation = result_list['BASE_UNCONDITIONALEXPECTATION'].load()
    # mrk_discount = result_list['BASE_FITTINGDISCOUNT'].load()
    # discount = result_list['BASE_MODEL_DISCOUNTBOND'].averave()
    # mrk_spot = result_list['BASE_FITTINGSPOT'].averave()
    # mrk_forward = result_list['BASE_FITTINGFORWARD'].averave()
    # rnd_z = result_list['BASE_RANDOMZ'].averave()

    # print(shortrate_aver)
    # print(shortrate[0])
    # print(shortrate[1])

    # plt.plot(discount)
    # plt.plot(mrk_discount)
    # plt.plot(mrk_spot)

    i = 0

    # for z, short_u_exp, short, spot, forward, mrk_disc, disc in zip(rnd_z, shortrate_uncon_expectation[0],
    #                                                                 shortrate_aver, mrk_spot, mrk_forward,
    #                                                                 mrk_discount[0], discount):
    #     print (
    #     str(i) + ' : ' + str(z) + ' , ' + str(short_u_exp) + ' , ' + str(short) + ' , ' + str(spot) + ' , ' + str(
    #         forward) + ' , ' + str(mrk_disc) + ' , ' + str(disc) + ' , ' + str(mrk_disc - disc))
    #     i += 1

    # plt.plot(shortrate_aver)
    # plt.plot(shortrate_uncon_expectation[0])
    plt.figure(1)
    plt.plot(res.timegrid.data['T'], shortrate.average(), label='shor_aver')
    plt.plot(res.timegrid.data['T'], shortrate_uncon_expectation.data[0], label='short_analytic')
    plt.title('short_aver vs short_analytic')
    plt.xlabel('time (year)')
    plt.ylabel('rate (%)')
    plt.legend()

    plt.figure(2)
    plt.plot(res.timegrid.data['T'], shortrate.average() - shortrate_uncon_expectation.data[0], label='diff')
    plt.title('short_aver - short_analytic')
    plt.xlabel('time (year)')
    plt.ylabel('rate (%)')
    plt.legend()

    # plt.plot(mrk_forward)
    # pos = 360
    # print(mrk_discount[0][pos])
    # print(discount[pos])
    #
    # print(mrk_discount[0][pos] - discount[pos])
    #
    # print('disc diff ' + str(pos) + ' : ' + str(mrk_discount[0][pos] - discount[pos]))

    plt.figure(3)
    plt.title('discount - mrk_discount')
    # plt.plot(mrk_discount[0])
    # plt.plot(discount)

    plt.plot(mrk_discount.data[0] - model_discount.average())

    plt.figure(4)
    plt.title('rand_z')
    plt.plot(rnd_z.average())
    #print('aver Z : ' + rnd_z))
    plt.show()
    # result_obj.load(1,1)
    # print result_obj.arr

    # market forward vs short rate aver

    # market forward vs t-measure short rate aver
    # alpha vs short rate aver
    # market disc vs disc aver

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
    scen.general.frequency = frequency.value

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