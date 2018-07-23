# coding=euc-kr
import xenarix as scen

def get_test_model(process_name):

    cali_id = 'cali_gbm'
    model = scen.GarmanKohlhagen(process_name)

    model.sections["X0"] = 100

    model.dom_rf_curve.tenor = ['3M', '6M', '9M', '12M', '24M', '36M', '48M', '60M', '120M', '180M']
    model.dom_rf_curve.value = [0.0164, 0.0161, 0.0159, 0.0164, 0.0173, 0.0182, 0.0191, 0.0218, 0.0229, 0.0229]
    model.for_rf_curve.tenor = ['100Y']
    model.for_rf_curve.value = [0.005]
    model.sigma_curve.tenor = ['5Y', '100Y']
    model.sigma_curve.value = [0.3, 0.2]

    return model


def test():
    model = scen.GarmanKohlhagen('gk_model')

    scen1 = scen.Scenario()
    scen1.add_model(model)
    scen1.save_as('gk_test')
    scen1.generate('gk_test', 'gk_result')

if __name__ == "__main__":
    test()