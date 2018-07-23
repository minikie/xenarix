# coding=euc-kr
import xenarix as scen

cali_id = 'cali_cir1f'


def get_test_model(process_name):

    model = scen.CIR1F(process_name)

    model.r0 = 0.03
    model.alpha = 0.1
    model.longterm = 0.1
    model.sigma = 0.01

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

    cali1 = scen.Calibrator()

    cali1.model = model
    cali1.calibrationtools = calibration_tools
    cali1.save_as(cali_id)
    # cali1.calibrate('testcali1')

    scen1 = scen.Scenario()
    scen1.add_model(model)
    scen1.save_as('cir1f_test')
    scen1.generate('cir1f_test', 'cir1f_result')

if __name__ == "__main__":
    _model = get_test_model('cir1f_process')
    test(_model)