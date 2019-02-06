# coding=utf-8
import os
from enum import Enum
from collections import OrderedDict
import json
import imp

#xen_bin_dir = os.environ['XENARIX_BINPATH'].replace(';', '')
xen_bin_dir = None


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