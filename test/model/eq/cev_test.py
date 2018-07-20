# coding=euc-kr
import xenarix as scen


def get_test_model(process_name):
    cali_id = 'cali_cev'
    model = scen.CEV(process_name)

    model.sections["X0"] = 100
    model.sections["RF_CURVE_TENOR"] = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M', '100Y']
    model.sections["RF_CURVE_VALUE"] = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229, 0.0229]

    model.sections["DIVIDEND_CURVE_TENOR"] = ['100Y']
    model.sections["DIVIDEND_CURVE_VALUE"] = [0.005]

    model.sections["SIGMA_CURVE_TENOR"] = ['5Y', '100Y']
    model.sections["SIGMA_CURVE_VALUE"] = [0.3, 0.2]

    model.sections["LEVERAGE"] = 1.0

    return model


def test(model):
    scen1 = scen.Scenario()
    scen1.add_model(model)
    scen1.save_as('cev_test')
    scen1.generate('cev_test', 'cev_result')

if __name__ == "__main__":
    _model = get_test_model('cev_process')
    test(_model)
