# coding=euc-kr
import xenarix as scen

def get_test_model(process_name):
    cali_id = 'cali_cevconst'
    model = scen.CEVConst(process_name)

    model.sections["X0"] = 100
    model.sections["RF"] = 0.03
    model.sections["DIVIDEND"] = 0.01
    model.sections["SIGMA"] = 0.3

    return model


def test(model):
    scen1 = scen.Scenario()
    scen1.add_model(model)
    scen1.save_as('cevconst_test')
    scen1.generate('cevconst_test', 'cevconst_result')

if __name__ == "__main__":
    _model = get_test_model('cevconst_process')
    test(_model)