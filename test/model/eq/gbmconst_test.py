# coding=euc-kr
import xenarix as scen

cali_id = 'cali_gbmconst'


def get_test_model(process_name):

    model = scen.GBMConst(process_name)

    model.x0 = 100
    model.sections["RF"] = 0.03
    model.sections["DIVIDEND"] = 0.01
    model.sections["SIGMA"] = 0.3

    return model


def test(model):
    scen1 = scen.Scenario()
    scen1.add_model(model)
    scen1.save_as('gbmconst_test')
    scen1.generate('gbmconst_test', 'gbmconst_result')

if __name__ == "__main__":
    _model = get_test_model('gbmconst_process')
    test(_model)