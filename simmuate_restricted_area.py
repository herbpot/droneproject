import simpy as si
import numpy as np
from simpy.events import Timeout

climate = int(np.random.randint(1,3))
climate = 0

if climate == 1 :
    climate = '비'
if climate == 2 :
    climate = '맑음'
if climate == 3 :
    climate = '바람'


def dron_1(env) : 

    global battery_1,hight_1,inertia_1,dron_gps_1,restricted_area_1,wight_1
    #battery_1 = 100 #드론 배터리 용량
    hight_1 = 10 #드론 높이
    #inertia_1 = 0 #관성구현용
    dron_gps_1 = [0,0] #드론 위치(GPS)
    #restricted_area_1 = [0,0] #제한구역 위치(GPS)
    #wight_1 = None #드론 무게
    #speed = 1 #낙하 속도
    jirosencer = 0
    
    
    while battery_1 > 0 : # 드론 높이 상승
        battery_1 = battery_1 - 1
        hight_1 = hight_1 + 1
        
    

    yield Timeout(1)


env = si.Environment()
env.process()
env.run()