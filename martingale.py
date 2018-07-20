import xenarix as xen
import results


class TestManager:
    def __init__(self, scen):
        self.scen = scen


class TestResult:
    def __init__(self):
        pass



class MartingaleTestReulst(TestResult):
    def __init__(self):
        TestResult.__init__()
        self.evolve_values = None
        self.expected_values = None

    def set_scenario(self, scen):
        result_list = results.xeResultList(set_name, scen.get_scen_id(), scen.get_result_id())



set_name = 'validation_test'
scen1 = xen.Scenario('test','test1')


# scenario를 받어서 거기 안에 들어있는거 전부?
# set_name을 martinagle_test 라고함?
def test_scenario_validation(scen):
    # 필요한 caluculation을 넣음
    for model in scen.models.values():
        #model.add_debug_calc('EXPECTATION')
        #model.add_calc(xen.UnconditionalExpectation())
        model.add_calc(xen.Expectation())
        #model.add_calc(xen.Ran())

        # model.add_calc('FITTINGDISCOUNT')


    # gen을함
    scen.generate(set_name)

    # analysys
    # analysys(scen)

    # report to html


def analysys(scen):
    result_list = results.xeResultList(set_name, scen.get_scen_id(), scen.get_result_id())

    for model in scen.models.values():
        MartingaleTestReulst()




def report(test_results):
    for result in test_results:
        pass
