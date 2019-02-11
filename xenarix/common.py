# coding=utf-8
import os
from enum import Enum
from collections import OrderedDict
import json
import imp
import numpy as np

#xen_bin_dir = os.environ['XENARIX_BINPATH'].replace(';', '')
xen_bin_dir = None

error_bound = 1.0e-10

def is_equal(x, y):
    if x-y < error_bound:
        return True
    else:
        return  False


def get_repository():
    global xen_bin_dir

    if xen_bin_dir == None:
        xen_bin_dir = os.path.join(os.getcwd(), 'repository')
        if os.path.exists(xen_bin_dir) == False:
            os.makedirs(xen_bin_dir)
            print ('default repository is initialized.')

        #raise Exception('repository is not initialized.')

    if os.path.exists(xen_bin_dir) == False:
        raise Exception(xen_bin_dir + ' repository does not exist.')

    return xen_bin_dir


def set_repository(dir, is_make_directory=True):
    global xen_bin_dir

    tf = os.path.exists(dir)
    if os.path.exists(dir) == False:
        if is_make_directory:
            os.makedirs(dir)
        else:
            raise Exception(dir + ' folder does not exist.')

    xen_bin_dir = dir


def check_directory(dir):
    if os.path.exists(dir) == False:
        os.makedirs(dir)
    return dir


def xen_input_dir(): return check_directory(get_repository() + "\\scen_input_file")
def xen_input_temp_dir(): return check_directory(get_repository() + "\\scen_input_file\\temp")
def xen_result_dir(): return check_directory(get_repository() + "\\scen_results")

def xen_cali_input_dir(): return check_directory(get_repository() + "\\cali_input_file")
def xen_cali_result_dir(): return check_directory(get_repository() + "\\cali_results")


xen_extension = '.xen'
cali_extension = '.cali'
xenset_extension = '.xens'

engine_filename = 'xenarix_engine.exe'
resultinfo_filename = 'RESULTINFO.TXT'
timegridinfo_filename = 'TIMEGRIDINFO.TXT'

module_dir_info = imp.find_module('xenarix')
engine_path = module_dir_info[1] + '\\' + engine_filename


class Interpolation(Enum):
    BackwardFlat = 'BACKWARDFLAT'
    ForwardFlat = 'FORWARDFLAT'
    Linear = 'LINEAR'
    LogLinear = 'LOGLINEAR'
    CubicNaturalSpline = 'CUBICNATURALSPLINE'
    LogCubicNaturalSpline = 'LOGCUBICNATURALSPLINE'
    MonotonicCubicNaturalSpline = 'MONOTONICCUBICNATURALSPLINE'
    MonotonicLogCubicNaturalSpline = 'MONOTONICLOGCUBICNATURALSPLINE'
    KrugerCubic = 'KRUGERCUBIC'
    KrugerLogCubic = 'KRUGERLOGCUBIC'
    FritschButlandCubic = 'FRITSCHBUTLANDCUBIC'
    FritschButlandLogCubic = 'FRITSCHBUTLANDLOGCUBIC'
    Parabolic = 'PARABOLIC'
    LogParabolic = 'LOGPARABOLIC'
    MonotonicParabolic = 'MONOTONICPARABOLIC'
    MonotonicLogParabolic = 'MONOTONICLOGPARABOLIC'


class Extrapolation(Enum):
    FLAT = 'FLAT'


class TimeGridFrequency(Enum):
    Day = 'DAY'
    Month = 'MONTH'
    Quarter = 'QUARTER'
    SemiAnnual = 'SEMIANNUAL'
    Annual = 'ANNUAL'
    FirstOfMonth = 'FIRSTOFMONTH'
    FirstOfQuarter = 'FIRSTOFQUARTER'
    FirstOfSemiannual = 'FIRSTOFSEMIANNUAL'
    FirstOfAnnual = 'FIRSTOFANNUAL'
    EndOfMonth = 'ENDOFMONTH'
    EndOfQuarter = 'ENDOFQUARTER'
    EndOfSemiannual = 'ENDOFSEMIANNUAL'
    EndOfAnnual = 'ENDOFANNUAL'


class RndType(Enum):
    Crude = 'CRUDE'
    Sobol = 'SOBOL'


class KeyValue:
    def __init__(self, line):
        s = line.split('=')
        self.key = s[0]
        self.value = None

        if s[1].find('(') > 0:
            self.value = []
            ss = s[1].replace('(', ' ')
            ss = ss.replace(')', ' ')
            rows = ss.split(',')

            for row in rows:
                self.value.append(filter(None, row.split('|')))

        elif s[1].find('|') > 0:
            self.value = filter(None, s[1].split('|'))
        else:
            self.value = s[1]


def value_to_string(v):
    s = ''
    if isinstance(v, list):
        if len(v) == 1:
            s = str(v[0])
        else:
            s = '|'.join([str(vv) for vv in v])
    else:
        s = str(v)

    return s


# entire input information , like DOM
class InputParser:
    def __init__(self, contents):
        self.contents = contents
        self.category_names = ['GENERATIONENVIROMENT', 'PROCESSINFO', 'SHOCKINFO', 'CALCULATIONINFO']
        self.categories = OrderedDict()

        for nm in self.category_names:
            self.categories[nm] = Category(nm)

        self.load_str(self.contents)

    def __setitem__(self, key, item):
        self.categories[key] = item

    def __getitem__(self, key):
        return self.categories[key]

    def load_str(self, contents):
        # category 별로 나눔
        contents = contents.replace('\n', '')
        contents = contents.replace(' ', '')
        for nm in self.category_names:
            s = contents[contents.find('#' + nm) + len(nm) + 1:contents.find('#' + nm + '_END')]
            self.categories[nm].category_name = nm
            self.categories[nm].load_str(s)


class Category:
    def __init__(self, category_name):
        self.category_name = category_name
        self.tags = []

    # 여러개 tag를 묶어서 내놓음
    def build(self):
        contents = ['#' + self.category_name]
        for tag in self.tags:
            contents.append(tag.build())

        contents.append('#' + self.category_name + '_END')
        contents.append('\n')

        return '\n'.join(contents)

    def json_dict(self):
        v = OrderedDict()
        for tag in self.tags:
            if tag.tag_name not in v:
                v[tag.tag_name] = []
                v[tag.tag_name].append(tag.sections)
            else:
                v[tag.tag_name].append(tag.sections)

        return v

    def load_str(self, contents):
        pos_start = contents.find('[')
        pos_end = contents.find(']')

        while pos_end != -1:
            pos_start_next = contents.find('[', pos_start + 1)
            if pos_start_next == -1:
                pos_start_next = len(contents)

            nm = contents[pos_start + 1:pos_end]
            tag_contents = contents[pos_start:pos_start_next]
            tag = Tag()
            tag.load_str(tag_contents)
            self.tags.append(tag)

            pos_start = pos_start_next
            pos_end = contents.find(']', pos_end + 1)


# 이게 []이걸로 묶인것
class Tag:
    def __init__(self, tag_name='unknown'):
        self.sections = OrderedDict()
        self.tag_name = tag_name
        self.tag_wrapper = '[]'

    # yield curve 같은 class 에서 sections 을 만들어냄
    def pre_build(self):
        pass

    # string from sections
    def build(self):
        self.pre_build()

        line = ['[{}]'.format(self.tag_name)]

        # if list 이면 해야댐.
        for k, v in self.sections.items():
            if k.find('MATRIX') > 0:
                s = '('
                for a in v:
                    s += '|'.join([str(e) for e in a])
                    s += ','
                s = s[:-1]
                s += ')'
                line.append(k + '=' + s + ';')
            elif isinstance(v, list):
                if len(v) == 1:
                    line.append(k + '=' + str(v[0]).upper() + '|;')
                else:
                    line.append(k + '=' + '|'.join(str(a) for a in v) + ';')
            else:
                line.append(k + '=' + str(v).upper() + ';')

        return '\n'.join(line)

    def build_json(self):
        return json.dumps(self.sections)

    def load_tag(self, tag):
        isinstance(tag, Tag)
        for key in self.sections.keys():
            self.sections[key] = tag.sections[key]

        return self

    def load_str(self, contents):
        pos_start = contents.find('[')
        pos_end = contents.find(']')
        self.tag_name = contents[pos_start + 1:pos_end]

        lines = contents[pos_end + 1:].split(';')

        for line in lines:
            if line != '':
                kv = KeyValue(line)
                self.sections[kv.key] = kv.value

        return self

    def set_sections(self, **kwargs):
        for k, v in kwargs.items():
            self.sections[k.upper()] = value_to_string(v).upper()


class Calculation(Tag):
    def __init__(self, calc_name):
        Tag.__init__(self, 'CALCULATION')
        self.sections['NAME'] = calc_name
        self.calc_name = calc_name
        self.calc_type = ''


class BuiltInCalculation(Calculation):
    def __init__(self, calc_name):
        Calculation.__init__(self, calc_name)


class Variable(Tag):
    def __init__(self, var_name):
        Tag.__init__(self, "VARIABLE")
        self.sections['NAME'] = var_name
        self.var_name = var_name

    def add_shockdef(self, shock_item):
        raise Exception('not implemented')


class ValueVariable(Variable):
    def __init__(self, var_name, value=100):
        Variable.__init__(self, var_name)
        self.value = value

        self.sections['VALUE'] = 1000
        self.sections['VAR_TYPE'] = 'VALUE'

        # self.sections['SHOCK:UP_MULTI:MULTIPLE'] = 1.1
        # self.sections['SHOCK:DOWN_MULTI:MULTIPLE'] = 0.9
        # self.sections['SHOCK:UP_ADD:ADD'] = 100
        # self.sections['SHOCK:DOWN_ADD:ADD'] = -100

    def add_shockdef(self, shock_item):
        nm_str = 'SHOCK_DEF' + ':' + shock_item.name.upper() + ':' + shock_item.type.upper()
        if shock_item.type == 'add' or shock_item.type == 'mul':
            self.sections[nm_str] = shock_item.value
        # elif shock_item.type == 'mul':
        #     self.sections[nm_str] = shock_item.value
        else:
            raise Exception('unknown shock_item type')


class YieldCurveVariable(Variable):
    def __init__(self, var_name):
        Variable.__init__(self, var_name)
        value = np.array([1000, 1000, 1000, 1000, 1000])
        self.sections['VALUE'] = value
        self.sections['VAR_TYPE'] = 'YIELDCURVE'

        self.sections['SHOCK:MULTIPLEUP:MULTIPLE'] = value * 1.1
        self.sections['SHOCK:MULTIPLEDOWN:MULTIPLE'] = value * 0.9
        self.sections['SHOCK:ADDUP:ADD'] = value + 100
        self.sections['SHOCK:ADDDOWN:ADD'] = value - 100


class VolCurveVariable(Variable):
    def __init__(self, var_name):
        Variable.__init__(self, var_name)
        tenor = ['3M', '6M', '9M', '1Y', '2Y']
        value = np.array([0.02, 0.02, 0.02, 0.02, 0.02])
        self.sections['VAR_TYPE'] = 'VOLCURVE'

        self.sections["FITTING_CURVE_TENOR"] = tenor
        self.sections["FITTING_CURVE_VALUE"] = value
        self.sections["FITTING_CURVE_INTERPOLATION"] = "LINEAR"
        self.sections['SHOCK:PARALLELMULTIPLEUP:MULTIPLE'] = value * 1.1
        self.sections['SHOCK:PARALLELMULTIPLEDOWN:MULTIPLE'] = value * 0.9
        self.sections['SHOCK:PARALLELADDUP:ADD'] = value + 0.01
        self.sections['SHOCK:PARALLELADDDOWN:ADD'] = value - 0.01


class ProcessModel(Tag):
    def __init__(self, model_name, model_type):
        Tag.__init__(self, "PROCESS")
        self.model_name = model_name
        self.model_type = model_type

        self.sections["NAME"] = self.model_name
        self.sections["MODEL_TYPE"] = self.model_type
        self.sections['CALCULATION'] = ['VALUE']

        self.calculations = OrderedDict()

    def is_category(self, category):
        pass

    def underlying_key(self):
        pass

    def underlying_shock_value(self, value):
        pass

    def factor(self):
        pass

    def check_type(self, calc):
        if isinstance(calc, BuiltInCalculation):
            return  False
        return True

    def add_shock(self, shock_name, target, value):
        key = target + ':SHOCK:' + shock_name
        self.sections[key] = value_to_string(value)

    def add_calc(self, calc):
        calc_name = calc.sections['NAME'].upper()

        # if not self.check_type(calc):
        #     raise Exception('not valid calculation')

        if calc_name not in self.sections['CALCULATION']:
            self.sections['CALCULATION'].append(calc_name)
            if not isinstance(calc, BuiltInCalculation):
                self.calculations[calc_name] = calc
        else:
            raise Exception('duplicated calculation')

    def add_builtin_calc(self, builtin_calc_nm):
        if builtin_calc_nm not in self.sections['CALCULATION']:
            self.sections['CALCULATION'].append(builtin_calc_nm)

    def clear_calc(self):
        self.sections['CALCULATION'] = ['VALUE']

    def pre_build_value(self, name, v):
        if isinstance(v, ValueVariable):
            self.sections[name] = v.value
            self.sections[name + '_REF'] = v.var_name
            self.sections[name + '_REF_USING'] = True
        else:
            self.sections[name] = v