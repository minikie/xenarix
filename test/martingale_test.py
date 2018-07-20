import results as xen_result
import matplotlib.pyplot as plt
import numpy as np

set_name = 'newSet'
scen_name = 'TESTSCENTEMPLATEID'
result_name = 'TESTRESULTID1'

print ('xeResultFile')
# xeResultFile( file_full_name ) -> object
# value_file_name = 'C:/xenbin/scen_results/debug/TESTSCENTEMPLATEID/TESTRESULTID1/20150902_TESTSCENTEMPLATEID_BASE_HW1F_VALUE.SCN'
# market_discount_file_name = 'C:/xenbin/scen_results/debug/TESTSCENTEMPLATEID/TESTRESULTID1/20150902_TESTSCENTEMPLATEID_BASE_HW1F_MODEL_DISCOUNTBOND_BASE_VALUE.SCN'
# discount_file_name = 'C:/xenbin/scen_results/debug/TESTSCENTEMPLATEID/TESTRESULTID1/20150902_TESTSCENTEMPLATEID_BASE_HW1F_FITTINGDISCOUNT.SCN'

result_list = xen_result.xeResultList(set_name, scen_name, result_name )

print (result_list)

result_list['BASE_FITTINGDISCOUNT'].load(1, 1)

shortrate_aver = result_list['BASE_nan'].averave()
shortrate = result_list['BASE_nan'].load()
shortrate_uncon_expectation = result_list['BASE_UNCONDITIONALEXPECTATION'].load()
mrk_discount = result_list['BASE_FITTINGDISCOUNT'].load()
discount = result_list['BASE_MODEL_DISCOUNTBOND'].averave()
mrk_spot = result_list['BASE_FITTINGSPOT'].averave()
mrk_forward = result_list['BASE_FITTINGFORWARD'].averave()
rnd_z = result_list['BASE_RANDOMZ'].averave()



# print(shortrate_aver)
# print(shortrate[0])
# print(shortrate[1])

# plt.plot(discount)
# plt.plot(mrk_discount)
# plt.plot(mrk_spot)

i=0

for z, short_u_exp, short, spot, forward, mrk_disc, disc in zip(rnd_z, shortrate_uncon_expectation[0], shortrate_aver, mrk_spot, mrk_forward, mrk_discount[0], discount):
    print (str(i) + ' : ' + str(z) + ' , ' + str(short_u_exp) + ' , ' + str(short) + ' , ' + str(spot) + ' , ' + str(forward)  + ' , ' + str(mrk_disc) + ' , ' + str(disc) + ' , ' + str(mrk_disc - disc))
    i+=1

# plt.plot(shortrate_aver)
# plt.plot(shortrate_uncon_expectation[0])
plt.figure(1)
plt.title('short_aver - short_analytic')
plt.plot(shortrate_aver - shortrate_uncon_expectation[0])

# plt.plot(mrk_forward)
pos = 360
print(mrk_discount[0][pos])
print(discount[pos])

print(mrk_discount[0][pos] - discount[pos])

print('disc diff ' + str(pos) + ' : ' + str(mrk_discount[0][pos] - discount[pos]))

plt.figure(2)
plt.title('discount - mrk_discount')
# plt.plot(mrk_discount[0])
# plt.plot(discount)

plt.plot(mrk_discount[0] - discount)

plt.figure(3)
plt.title('rand_z')
plt.plot(rnd_z)
print('aver Z : ' + str(np.average(rnd_z)))
plt.show()
# result_obj.load(1,1)
# print result_obj.arr

# market forward vs short rate aver



# market forward vs t-measure short rate aver
# alpha vs short rate aver
# market disc vs disc aver