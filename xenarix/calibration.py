# coding=utf-8
from common import *
import datetime


class CalibrationTool(Tag):
    def __init__(self, tool_name):
        Tag.__init__(self, 'CALIBRATIONTOOL')
        self.sections['NAME'] = tool_name
        self.tool_name = tool_name
        self.type = ''


class CapTool(CalibrationTool):
    def __init__(self, tool_name, **kwargs):
        CalibrationTool.__init__(self, tool_name)

        self.sections['CALIBRATION_TOOL_TYPE'] = 'CAP'

        self.discount_curve = YieldCurve()
        self.value = 0.3

        self.tenor = '1Y'
        self.strike = 1.0
        self.value_type = 'black'

    def pre_build(self):
        #self.sections.update(self.discount_curve.make_sections('DISCOUNT'))

        self.sections['CAP_VOL_TENOR'] = self.tenor
        self.sections['CAP_VOL_STRIKE'] = self.strike
        self.sections['CAP_VOL_VALUE'] = self.value
        self.sections['CAP_VOL_VALUE_TYPE'] = self.value_type

        self.sections['REF_INDEX'] = 'IRSKRW'


class SwaptionTool(CalibrationTool):
    def __init__(self, tool_name, **kwargs):
        CalibrationTool.__init__(self, tool_name)
        self.sections['CALIBRATION_TOOL_TYPE'] = 'SWAPTION'

        self.discount_curve = YieldCurve()
        self.value = 0.3

        self.swap_maturity = '1Y'
        self.tenor = '1Y'
        self.strike = 1.0
        self.value_type = 'black'


    def pre_build(self):
        #self.sections.update(self.discount_curve.make_sections('DISCOUNT'))

        self.sections['SWAPTION_VOL_TENOR'] = self.tenor
        self.sections['SWAPTION_VOL_SWAPMATURITY'] = self.swap_maturity
        self.sections['SWAPTION_VOL_STRIKE'] = self.strike
        self.sections['SWAPTION_VOL_VALUE'] = self.value
        self.sections['SWAPTION_VOL_VALUE_TYPE'] = self.value_type

        self.sections['REF_INDEX'] = 'IRSKRW'


class UnknownCalibrationTool(CalibrationTool):
    pass


def make_swaption(option_maturity='1Y', swap_maturity='1Y', value=0.3, strike=0.1, value_type='black'):
    pass


def make_swaptions(option_maturities,
                   swap_maturities,
                   values,
                   strikes,
                   value_type='black'):

    if not len(option_maturities) == len(swap_maturities) == len(values) == len(strikes):
        raise Exception('array length does not equal')

    swaptions = []

    for om, sm, v, st in zip(option_maturities, swap_maturities, values, strikes):
        tool_name = 'SWAPTION_' + om + '_' + sm + '_' + str(st)
        swaption = SwaptionTool(tool_name)

        swaption.tenor = om
        swaption.swap_maturity = sm
        swaption.strike = st
        swaption.value = v

        swaptions.append(swaption)

    return swaptions

# values_matrix
# row = swap_maturity
# col = option_maturity
def make_swaptions_from_matrix(swap_maturities,
                               option_maturities,
                               values_matrix,
                               level_strike=0.015,
                               value_type='black'):
    if len(values_matrix) == 0:
        raise Exception('values_matrix is empty')

    if not len(swap_maturities) == len(values_matrix):
        raise Exception('swap maturities length is not matched to values_matrix row length')

    if not len(option_maturities) == len(values_matrix[0]):
        raise Exception('swap maturities length is not matched to values_matrix row length')

    swaptions = []

    for i, sm in enumerate(swap_maturities):
        for j, om in enumerate(option_maturities):
            tool_name = 'SWAPTION_' + om + '_' + sm + '_' + str(level_strike)
            swaption = SwaptionTool(tool_name)

            swaption.tenor = om
            swaption.swap_maturity = sm
            swaption.strike = level_strike
            swaption.value = values_matrix[i][j]

            swaptions.append(swaption)

    return swaptions


def make_swaptions_from_cube(row_option_maturities=['1Y'],
                               col_swap_maturities=['1Y'],
                               values_matrix=[[0.3]],
                               strike='atm',
                               value_type='black'):
    pass



def get_calibrationtool(tag):
    isinstance(tag, Tag)
    # if tag.tag_name != '':
    #     return None

    tool_type = tag.sections['CALIBRATION_TOOL_TYPE']
    tool_name = tag.sections['NAME']

    if tool_type == "CAP":
        return CapTool(tool_name).load_tag(tag)
    elif tool_type == "SWAPTION":
        return SwaptionTool(tool_name).load_tag(tag)
    else:
        return UnknownCalibrationTool(tool_name)


class CalibrationGeneral(Tag):
    def __init__(self):
        Tag.__init__(self, "CALIBRATIONGENERAL")

        self.calibration_id = "TESTSCENID1"
        self.reference_date = "20150902"
        self.result_id = "TESTRESULTID1"


    def pre_build(self):
        self.sections["CALIBRATION_ID"] = self.calibration_id
        self.sections["RESULT_ID"] = self.result_id
        self.sections["REFERENCE_DATE"] = self.reference_date


class Calibrator:
    def __init__(self, cali_name, model, result_name, calibration_tools):
        self.contents = ''
        self.calibration_enviroment_category = Category('CALIBRATIONENVIROMENT')
        self.calibrationinfo_category = Category('CALIBRATIONINFO')

        self.general = CalibrationGeneral()

        self.general.calibration_id = cali_name
        self.general.result_id = result_name

        if not (isinstance(model, CalibrationProcessModel) and isinstance(model, ProcessModel)):
            raise Exception('CalibrationProcessModel is needed')

        self.model = model
        self.calibrationtools = OrderedDict()

        for tool in calibration_tools:
            self.calibrationtools[tool.tool_name] = tool


    def save(self):
        self.build()
        timestamp_str = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        filename = self.general.result_id  + '_' + timestamp_str + cali_extension
        f = open(xen_cali_input_dir() + '\\' + filename, 'w')
        f.write(self.contents)
        f.close()

        return filename

    def load(self, id):
        fpath = xen_cali_input_dir() + '\\' + id + xen_extension
        if not os.path.exists(fpath):
            raise IOError()

        f = open(fpath, 'r')

        contents = f.read()

        self.load_contents(contents)

    def load_contents(self, contents):

        self.contents = contents

        # dom 을 만듬
        inputParser = InputParser(self.contents)
        # dom 에서 generalenv 을 가져옴

        for env_tag in inputParser['GENERATIONENVIROMENT'].tags:
            if env_tag.tag_name == 'GENERAL':
                self.general.load_tag(env_tag)

        # for 문을 돌려서 TOOL FACTORY로 정보를 계속 박음
        for cali_tag in inputParser['CALIBRATIONINFO'].tags:
            if cali_tag.tag_name == 'CALIBRATIONTOOL':
                tool = get_calibrationtool(cali_tag)
                if isinstance(tool, UnknownCalibrationTool):
                    raise Exception('unknown model type : {}'.format(tool.type))
                if tool.tool_name not in self.calibrationtools:
                    self.calibrationtools[tool.tool_name] = tool
                elif tool.tool_name in self.calibrationtools:
                    raise Exception('duplicated model name : {}'.format(tool.tool_name))

            # elif cali_tag.tag_name == 'PROCESS':
            #     model = get_model(cali_tag)
            #     if isinstance(model, UnknownModel):
            #         raise Exception('unknown model type : {}'.format(model.model_type))
            #     self.model = model

    def build(self):
        self.contents = ""

        del self.calibration_enviroment_category.tags[:]
        del self.calibrationinfo_category.tags[:]

        self.calibration_enviroment_category.tags.append(self.general)

        self.calibrationinfo_category.tags.append(self.model)

        for tool in self.calibrationtools.values():
            self.calibrationinfo_category.tags.append(tool)

        self.contents = self.calibration_enviroment_category.build() \
                      + self.calibrationinfo_category.build()

    def dump(self):
        self.build()
        return self.contents

    def calibrate(self):
        filename = self.save()

        arg_str = ['--cali',
                   '--repo={}'.format(get_repository()),
                   '--file={}'.format(filename)]

        run_command = engine_path + ' ' + ' '.join(arg_str)
        print(run_command)
        res = os.system(run_command)