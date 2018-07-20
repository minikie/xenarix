# coding=euc-kr
import xenarix as scen
import numpy as np

cali_id = 'cali_gbm'


def get_test_model(process_name):

    model = scen.GBMLocalVol(process_name)
    x0 = 100
    model.sections["X0"] = x0
    model.sections["RF_CURVE_TENOR"] = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M', '100Y']
    model.sections["RF_CURVE_VALUE"] = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229, 0.0229]

    model.sections["DIVIDEND_CURVE_TENOR"] = ['100Y']
    model.sections["DIVIDEND_CURVE_VALUE"] = [0.005]

    model.sections["SIGMA_SURFACE_TENOR"] = ['1Y', '2Y', '3Y', '4Y', '5Y', '100Y']
    model.sections["SIGMA_SURFACE_STRIKE"] = (x0 * np.array([0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4])).tolist()

    model.sections["SIGMA_SURFACE_MATRIX"] = [[0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
                                             [0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
                                             [0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
                                             [0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
                                             [0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
                                             [0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
                                             [0.3, 0.29, 0.28, 0.27, 0.26, 0.26]]
    return model


def test(model):
    scen1 = scen.Scenario()
    scen1.add_model(model)
    scen1.save_as('gbmlocalvol_test')
    scen1.generate('gbmlocalvol_test', 'gbmlocalvol_result')

if __name__ == "__main__":
    _model = get_test_model('gbmlocalvol_process')
    test(_model)