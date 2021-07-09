# import simpy
	    
# def car(env):
#     """
#     자동차 프로세스
#     주차하고 여행을 떠남
#     parking과 driving 상태를 스위칭함
#     """
#     while True:
#         print('Start parking at %d' % env.now)
#         parking_duration = 5
#                 # 환경에서 timeout 이벤트를 발생시킴(parking_duration동안 휴면)
#         yield env.timeout(parking_duration)	    
#         print('Start driving at %d' % env.now)
#         trip_duration = 2
#         yield env.timeout(trip_duration)
	    
# env = simpy.Environment()
# env.process(car(env))
# env.run(until=15)

import simpy as si

'''하나의 드론은 일반 배터리 내장 다른 드론은 지속적인 충전을 구현 '''





def dron_1(env) :
    global battery_1,hight_1,inertia_1,dron_gps_1,restricted_area_1
    battery_1 = 100 #드론 배터리 용량
    hight_1 = 0 #드론 높이
    inertia_1 = 0 #관성구현용
    dron_gps_1 = [0,0] #드론 위치(GPS)
    restricted_area_1 = [0,0] #제한구역 위치(GPS)
    """
    1번 드론
    """
    while battery_1 == 0 :
        battery_1 = battery_1 - 1
        dron_gps_1[0] = dron_gps_1[0] + 1
        print('드론 1이 간 거리' + str(dron_gps_1))
        print('남은 배터리 :' + str(battery_1))
        yield env.timeout(1)


    



def dron_2(env) :
    global battery_2,hight_2,inertia_2,dron_gps_2,restricted_area_2
    battery_2 = 100 #드론 배터리 용량
    hight_2 = 0 #드론 높이
    inertia_2 = 0 #관성
    dron_gps_2 = [0,0] #드론 위치(GPS)
    restricted_area_2 = [0,0] #제한구역 위치(GPS)

    """
    2번 드론
    """
    while battery_2 == 0 :
        for i in range(4) :
            battery_2 = battery_2 - 1
            dron_gps_2[0] = dron_gps_2[0] + 1
        battery_2 = battery_2 + 1
        print('드론 2가 간 거리' + str(dron_gps_2))
        print('남은 배터리 :' + str(battery_2))
        yield env.timeout(1)



env = si.Environment()
env.process(dron_1(env))
env.run()
