# coding=euc-kr
import xenarix as scen

cali_id = 'cali_g2ext'


def get_test_model(process_name):
    model = scen.G2Ext(process_name)

    model.sections["FITTING_CURVE_TENOR"] = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M', '100Y']
    model.sections["FITTING_CURVE_VALUE"] = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229, 0.0229]

    model.sections["PARA_ALPHA1_TENOR"] = ['36M']
    model.sections["PARA_SIGMA1_TENOR"] = ['12M', '24M', '36M']
    model.sections["PARA_ALPHA2_TENOR"] = ['36M']
    model.sections["PARA_SIGMA2_TENOR"] = ['12M', '24M', '36M']

    model.sections["PARA_ALPHA1_VALUE"] = [0.1]
    model.sections["PARA_SIGMA1_VALUE"] = [0.01, 0.01, 0.01]
    model.sections["PARA_ALPHA2_VALUE"] = [0.1]
    model.sections["PARA_SIGMA2_VALUE"] = [0.01, 0.01, 0.01]

    model.sections["PARA_ALPHA1_FIXES"] = [False]
    model.sections["PARA_SIGMA1_FIXES"] = [False, False, False]
    model.sections["PARA_ALPHA2_FIXES"] = [True]
    model.sections["PARA_SIGMA2_FIXES"] = [True, True, True]

    model.sections["CORR"] = 0.0

    model.add_calc(scen.XFirstFactor())
    model.add_calc(scen.YSecondFactor())
    #model.add_calc(scen.FittingTheta())
    #model.add_calc(scen.FittingAlpha())
    #model.add_calc(scen.FittingForward())
    #model.add_calc(scen.FittingSpot())
    #model.add_calc(scen.FittingDiscount())

    return model


def test(model):
    calibration_tools = dict()

    calibration_tools['cap1'] = scen.CapTool('cap1')
    calibration_tools['cap1'].sections['DISCOUNT_CURVE_VALUE'] = [0.03, 0.031, 0.032, 0.033]
    calibration_tools['cap1'].sections['DISCOUNT_CURVE_TENOR'] = ['1Y', '2Y', '3Y', '4Y']
    calibration_tools['cap1'].sections['DISCOUNT_CURVE_INTERPOLATION'] = 'MONOTONICCUBICNATURALSPLINE'

    calibration_tools['cap1'].sections['CAP_VOL_CURVE_VALUE'] = [0.155, 0.160, 0.158, 0.156]
    calibration_tools['cap1'].sections['CAP_VOL_CURVE_TENOR'] = ['12M', '24M', '36M', '48M']
    calibration_tools['cap1'].sections['CAP_VOL_CURVE_STRIKE'] = 0.03
    calibration_tools['cap1'].sections['REF_INDEX'] = 'IRSKRW'

    cali1 = scen.Calibrator()

    cali1.model = model
    cali1.calibrationtools = calibration_tools
    cali1.save_as(cali_id)
    # cali1.calibrate('testcali1')

    scen1 = scen.Scenario()
    scen1.add_model(model)
    scen1.refresh_corr()
    scen1.save_as('g2ext_test')
    scen1.generate('g2ext_test', 'g2ext_result')

if __name__ == "__main__":
    _model = get_test_model('g2ext_process')
    test(_model)