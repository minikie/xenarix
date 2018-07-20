# # coding=euc-kr
# import xenarix as scen
#
# scen1 = scen.get_scenario('testnewid')
# res = scen1.get_result('testresultid')
#
#
# scen1.get_shock_list()
#
# under_shk = scen1.get_shock('shock_name', type='underlying', category='all')
# # under_shk = scen.get_shock('shock_name', type='underlying', category='eq')
# # under_shk = scen.get_shock('shock_name', type='underlying', category='ir')
# # under_shk = scen.get_shock('shock_name', type='underlying', category='fx')
#
# under_shk.set('shock_name1', value=0.01)
#
# custom_shk = scen1.get_shock('prossesshock_name', type='custom')
#
# custom_shk.set('shock_name2', model_name='krwcd1', fitting_curve_value=[0.01, 0.01])
#
#
# scen1.add_shock(under_shk)
# scen1.add_shock(custom_shk)
#
# # calculation
#
# bond1 = scen.ZeroBond('bond1', notional=1.0, maturity='3Y', out_value_type='value')
# vanilla_option1 = scen.VanillaOption('vanilla_option1', notional=1.0, strike=0.95)
#
#
# scen1.add_calc(bond1, model_name='krwcd1')
# scen1.add_calc(vanilla_option1, model_name='krwcd1')
#
# scen1.save_as('testshocknewid')
#
# # scen1.generate('testshocknewid', 'shocktestres')
#
# # model에 있는건 안지움. ( 다른곳에서 쓸수도 있으니까)
# # under_shk.clear_shock()
#
# # model에 있는것 까지 죄다 지움.
# # scen1.clear_shock()
#
# # under_shk = scen1.get_shock('shock_name', type='volatility')
#
#
# model = scen.HullWhite1F('calimodel')
#
# calibration_tools = dict()
#
# calibration_tools['cap1'] = scen.CapTool('cap1')
# calibration_tools['cap2'] = scen.CapTool('cap2')
# calibration_tools['cap3'] = scen.CapTool('cap3')
#
# # cali1 = scen.get_calibrator('testcali1')
#
# cali1 = scen.Calibrator()
#
# cali1.model = model
# cali1.calibration_tools = calibration_tools
#
# cali1.calibrate('testcali1')
#
#
#
#
#
# #under_shk.add('krwcd_1', 'name2', fitting_curve_value=[0.01, 0.01])
#
#
# # [PROCESSSHOCK]
# # NAME=TESTSHOCK_1;
# # SHOCK_REF:CD91=NAME1|NAME2;
# # SHOCK_REF:KOSPI200=NAME1|NAME2;
# #
# # FITTING_CURVE_VALUE:SHOCK:NAME1=-0.01|-0.01|0.01|0.01|0.01|0.01|0.01|0.01|0.01|0.01|0.01;
# # FITTING_CURVE_VALUE:SHOCK:NAME2=-0.02|-0.02|0.02|0.02|0.02|0.01|0.01|0.01|0.01|0.01|0.01;
# # ALPHA:SHOCK:NAME3=0.01;
# #
# #
# # #CALCULATIONINFO
# # [CALCULATION]
# # NAME=SPOT1;
# # CALC_TYPE=SPOT;
# # MODEL_CATEGORY=IR;
# # MATURITY=10Y;
# # OUT_VALUE_TYPE=VALUE;
# #
# #
# #
# # [CALCULATION]
# # NAME=FORWARD1;
# # CALC_TYPE=FORWARD;
# # MODEL_CATEGORY=IR;
# # MATURITY=10Y;
# # FORWARD_PERIOD=3M;
# # OUT_VALUE_TYPE=VALUE;
# #
# #
# # [CALCULATION]
# # NAME=DISCOUNT1;
# # CALC_TYPE=DISCOUNT;
# # MODEL_CATEGORY=IR;
# # MATURITY=10Y;
# # OUT_VALUE_TYPE=VALUE;
# #
# #
# # [CALCULATION]
# # NAME=ZERO_BOND1;
# # CALC_TYPE=ZERO_BOND;
# # MODEL_CATEGORY=IR;
# # NOTIONAL=1.0;
# # MATURITY=10Y;
# # CONST_MATRITY=TRUE;
# # ROLLOVER=TRUE;
# # OUT_VALUE_TYPE=VALUE;
# # OUT_VALUE_TYPE=DURATION;
# # OUT_VALUE_TYPE=CONVEXITY;
# # OUT_VALUE_TYPE=PRICE;
# #
# #
# #
# # [CALCULATION]
# # NAME=FIXED_BOND1;
# # CALC_TYPE=FIXED_BOND;
# # MODEL_CATEGORY=IR;
# # NOTIONAL=1.0;
# # MATURITY=10Y;
# # COUPON_TENOR=3M;
# # COUPON_RATE=0.03;
# # DAYCOUNTER=ACTACT;
# # COMPOUNDING=ANNUAL;
# # ROLLOVER=TRUE;
# # OUT_VALUE_TYPE=DURATION;
# # OUT_VALUE_TYPE=VALUE;
# # OUT_VALUE_TYPE=PRICE;
# #
# #
# #
# # [CALCULATION]
# # NAME=FLOATING_BOND1;
# # CALC_TYPE=FLOATING_BOND;
# # MODEL_CATEGORY=IR;
# # NOTIONAL=1.0;
# # MATURITY=10Y;
# # COUPON_TENOR=3M;
# # GEARING=1.0;
# # SPREADE=0.01;
# # DAYCOUNTER=ACTACT;
# # COMPOUND=ANNUAL;
# # ROLLOVER=TRUE;
# # OUT_VALUE_TYPE=DURATION;
# # OUT_VALUE_TYPE=VALUE;
# # OUT_VALUE_TYPE=PRICE;
# #
# #
# # [CALCULATION]
# # NAME=INVERSE_FLOATING_BOND1;
# # CALC_TYPE=INVERSE_FLOATING_BOND;
# # MODEL_CATEGORY=IR;
# # NOTIONAL=1.0;
# # MATURITY=10Y;
# # COUPON_TENOR=3M;
# # FIXED_RATE=0.04;
# # GEARING=1.0;
# # SPREADE=0.01;
# # DAYCOUNTER=ACTACT;
# # COMPOUND=ANNUAL;
# # ROLLOVER=TRUE;
# # OUT_VALUE_TYPE=DURATION;
# # OUT_VALUE_TYPE=VALUE;
# # OUT_VALUE_TYPE=PRICE;
# #
# #
# # [CALCULATION]
# # NAME=VANILLA_EQ_OPTION1;
# # CALC_TYPE=VANILLA_EQ_OPTION;
# # MODEL_CATEGORY=EQ;
# # PRICING_MODEL=BLACK;
# # NOTIONAL=1.0;
# # MATURITY=3M;
# # ROLLOVER=TRUE;
# # VOL=0.3;
# # STRIKE=1000;
# # OUT_VALUE_TYPE=DELTA;
# # OUT_VALUE_TYPE=VALUE;
# # OUT_VALUE_TYPE=PRICE;
# #
# # [CALCULATION]
# # NAME=BARRIER_EQ_OPTION1;
# # CALC_TYPE=BARRIER_EQ_OPTION;
# # MODEL_CATEGORY=EQ;
# # PRICING_MODEL=BLACK;
# # NOTIONAL=1.0;
# # MATURITY=3M;
# # ROLLOVER=TRUE;
# # VOL=0.3;
# # STRIKE=1000;
# # OUT_VALUE_TYPE=DELTA;
# # OUT_VALUE_TYPE=VALUE;
# # OUT_VALUE_TYPE=PRICE;
# #
# #
# #
# # [CALCULATION]
# # NAME=HIST_VOL1;
# # CALC_TYPE=HIST_VOL;
# # MODEL_CATEGORY=ALL;
# # AVER_PEORIOD=1Y;
# #
# #
# # [CALCULATION]
# # NAME=EWMA_VOL1;
# # CALC_TYPE=EWMA_VOL;
# # MODEL_CATEGORY=ALL;
# # AVER_PEORIOD=1Y;
# # LAMBDA=0.9;
# #
# #
# # [CALCULATION]
# # NAME=CASH1;
# # CALC_TYPE=CASH;
# # MODEL_CATEGORY=IR;
# # NOTIONAL=1.0;
# # COMPOUND=ANNUAL;
# # SPREAD=0.01;
# #
# #
# #
# # [CALCULATION]
# # NAME=CASH1;
# # CALC_TYPE=CASH;
# # MODEL_CATEGORY=IR;
# # NOTIONAL=1.0;
# # COMPOUND=ANNUAL;
# # SPREAD=0.01;
# #
# #
# #
# # #CALCULATIONINFO_END
# #
# #
# #
#
#
#
#
#
#
#
#
