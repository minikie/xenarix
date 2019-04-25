import datetime

def datetime_to_datestr_yyyymmdd(date):
    return date.strftime('%Y%m%d')

def datetime_to_datestr_iso(date):
    return date.strftime('%Y-%m-%d')