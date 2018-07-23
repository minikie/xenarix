# coding=euc-kr
import xenarix as scen
import numpy as np

cali_id = 'cali_gbm'


def get_test_model(process_name):

    model = scen.GBMLocalVol(process_name)
    model.x0 = 100

    model.rf_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
    model.rf_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]
    model.div_curve.tenor = ['100Y']
    model.div_curve.value = [0.005]

    model.sigma_surface.tenor = ['1Y', '2Y', '3Y', '4Y', '5Y', '100Y']
    model.sigma_surface.strike = (model.x0 * np.array([0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4])).tolist()

    model.sigma_surface.matrix = [[0.3, 0.29, 0.28, 0.27, 0.26, 0.26],
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