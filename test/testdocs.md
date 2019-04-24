## Test 항목

### unit test

#### general info

pass criteria
error : 각 옵션들 잘 먹는가.
logic : 각 옵션들 마다 테스팅 criteria 필요함.

scenario_id : 생성했을 때 파일 폴더 이름이 같음, resultinfo 에 확인
reference_date = 생성했을 때 파일이름 앞에 표기, timegrid 파일 내 시작 날짜 확인, resultinfo 에 확인
scenario_num = resultinfo 에 확인
delimiter = 사용 안하므로 pass
maxyear = timegrid 파일 내 시작 날짜 확인, resultinfo 에 확인
n_peryear = 사용 되었을 때, resultinfo 에 확인
rnd_type = 생성할 때 에러 안나는가
rnd_subtype = 생성할 때 에러 안나는가
rnd_seed = 생성할 때 에러 안나는가
rnd_skip = 설정한 값대로 시나리오가 잘 skip 되었는가
moment_match = random aver 가 0에잘 붙었는가
frequency = timegrid 파일 내 frequency를 계산해봄
frequency_month = 사용 되었을 때, timegrid 파일 내 day가 잘 고정되었는가
frequency_day = 사용 되었을 때, timegrid 파일 내 day가 잘 고정되었는가
result_id = 생성했을 때 파일 폴더 이름이 같음, resultinfo 에 확인
base_currency = 사용 안하므로 pass
thread_num = 나중에 검토

#### model generation

* hull white
* gbm
* gbmconst
* vasicek
* heston
* bk
* cir
* gk

- sample model
- using variable model (for several market data set)

pass criteria
analytic avaerage converge

#### pricing
상품 선정 ( price 먼저, greek은 나중에)
1. kospi2 call, put option
2. stepdown els
3. dls
4. fx option

그... simul num 줄여가면서 수렴도 체크

여기서 incubating을 여기 project에서 하고,
추후에 잘 packaging 해서 mxdevtool로 보냄

#### shock
* value add
* yield curve add
* vol curve add

pass criteria
shocked analytic avaerage converge
base 대비 shock된 게 유지되는가 average 구했을 때 유지되는가


#### resultl load

pass criteria
로드가 잘 되는 가
각 함수가 잘 call 되어서 나오는가

#### correlation

모델 전체 

pass criteria
[-1.0 ~ 1.0] 사이에 있는가
함수가 잘 에러 없이 동작하는가
사후 correlation이 잘 붙는가




#### graph view

pass criteria


#### calibration







