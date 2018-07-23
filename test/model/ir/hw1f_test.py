# coding=euc-kr
import xenarix as scen

cali_id = 'cali_hw1f'


def get_test_model(process_name):

    model = scen.HullWhite1F(process_name)

    #model.fitting_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
    #model.fitting_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]

    model.fitting_curve.tenor = ['1D', '3M', '6M', '12M', '24M', '30M']
    model.fitting_curve.value = [0.0147, 0.01664, 0.01631, 0.01625, 0.01638, 0.01652]

    model.alpha_curve.tenor = ['36M']
    model.alpha_curve.value = [0.1]
    model.sigma_curve.tenor = ['12M', '24M', '36M']
    model.sigma_curve.value = [0.01, 0.01, 0.01]

    model.sections["PARA_ALPHA_FIXES"] = [False]
    model.sections["PARA_SIGMA_FIXES"] = [False, False, False]

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
    calibration_tools['cap1'].sections['REF_INDEX'] = 'CD91'

    #calibration_tools['cap2'] = scen.CapTool('cap2')
    #calibration_tools['cap2'].sections['CAP_VOL_CURVE_VALUE'] = [0.32, 0.33, 0.34, 0.35]
    #calibration_tools['cap2'].sections['CAP_VOL_CURVE_TENOR'] = ['12M', '24M', '36M', '48M']
    #calibration_tools['cap2'].sections['CAP_VOL_CURVE_STRIKE'] = 0.04

    #calibration_tools['cap3'] = scen.CapTool('cap3')
    #calibration_tools['cap3'].sections['CAP_VOL_CURVE_VALUE'] = [0.35, 0.36, 0.37, 0.38]
    #calibration_tools['cap3'].sections['CAP_VOL_CURVE_TENOR'] = ['12M', '24M', '36M', '48M']
    #calibration_tools['cap3'].sections['CAP_VOL_CURVE_STRIKE'] = 0.05

    # cali1 = scen.get_calibrator('testcali1')

    cali1 = scen.Calibrator()

    cali1.model = model
    cali1.calibrationtools = calibration_tools
    cali1.save_as(cali_id)
    # cali1.calibrate('testcali1')

    scen1 = scen.Scenario()
    scen1.add_model(model)
    scen1.save_as('hw1f_test')
    scen1.generate('hw1f_test', 'hw1f_result')

if __name__ == "__main__":
    _model = get_test_model('hw1f_process')
    test(_model)