# coding=euc-kr
import xenarix as scen

cali_id = 'cali_heston'


def get_test_model(process_name):
    model = scen.HESTON(process_name)

    model.sections["X0"] = 100
    model.rf_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
    model.rf_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]
    model.div_curve.tenor = ['100Y']
    model.div_curve.value = [0.005]

    # parameter from http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.631.9340&rep=rep1&type=pdf
    # heston paper 1993
    model.v0 = 0.01
    model.kapa = 2
    model.long_variance = 0.01
    model.volofvol = 0.1
    model.rho = 0.0

    return model


def test(model):
    scen1 = scen.Scenario()
    scen1.add_model(model)
    scen1.refresh_corr()
    scen1.save_as('heston_test')

    scen1.generate('heston_test', 'heston_result')

if __name__ == "__main__":
    _model = get_test_model('heston_process')
    test(_model)