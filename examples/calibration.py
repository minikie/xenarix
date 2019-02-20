# coding=utf-8
import xenarix as xen
import xenarix.sample as xen_s
import xenarix.calibration as xen_cali
import xenarix.results as xen_r

xen.set_repository('c:\\xenarix')

calibration_instruments = []
# 1/3/2019 2/18/2019 10:22:08 AM
swap_maturity = ['1Y', '2Y', '3Y', '4Y', '5Y', '7Y', '10Y'] # swap_maturity
option_maturity = ['1Y', '2Y', '3Y', '5Y', '7Y', '10Y'] # option_maturity
swaption_data = [
[0.182, 0.227, 0.2355, 0.2555, 0.2415, 0.2295],
[0.202, 0.232, 0.238, 0.2455, 0.2295, 0.2185],
[0.221, 0.2395, 0.2355, 0.238, 0.222, 0.214],
[0.243, 0.2455, 0.236, 0.2315, 0.2155, 0.2135],
[0.258, 0.252, 0.2365, 0.228, 0.212, 0.212],
[0.257, 0.249, 0.231, 0.228, 0.216, 0.223],
[0.2525, 0.247, 0.228, 0.229, 0.226, 0.236]
]

hw1f_test = xen_s.hw1f(model_name='hw1f_test')
hw1f_test.set_cali_parameter_fix(alpha=True, sigma=False)


# 데이터가 있어야지
# swaption = xen_cali.make_swaption(option_maturity='1Y')
# swaptions = xen_cali.make_swaptions(option_maturities=['1Y'])

swaptions = xen_cali.make_swaptions_from_matrix(swap_maturities=swap_maturity,
                                                option_maturities=option_maturity,
                                                values_matrix=swaption_data)

# swaptions = xen_cali.make_swaptions_from_cube(row_option_maturities=['1Y'])

# cap = xen_cali.make_cap(maturity='1Y')
# caps = xen_cali.make_cap(maturity=['1Y'])

# calibration_instruments.append(swaption)


# 준비끝 cali 시작
cali_obj = xen_cali.Calibrator(cali_name='test_calibration',
                               model=hw1f_test,
                               result_name='test',
                               calibration_tools=swaptions)

# print cali_obj.dump()

cali_obj.calibrate()


# ~~~ 결과 ~~~~


# 결과 받어야지
calires_obj = xen_r.CaliResultObj(cali_name='test_calibration',
                               model_name=hw1f_test.model_name,
                               result_name='test')


# cali_obj.model
# cali_obj.error
# cali_obj.params # dict?
# cali_obj



