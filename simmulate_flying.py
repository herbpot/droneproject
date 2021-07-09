import simpy as si
import time as ti
import random
import pandas as pd


#변수 ################################################################
end_gps = [130,0] #목적지 위치
key_M = []
dron_sen_hp = []
l = {}
dron_hp = []

endcode = 0
climate = 0
windtime = 0
windforce = 0
hp = 0
dron_gps = [0,0] #드론 위치(GPS)
a = 0
done = 0
done_1 = 0
done_2 = 0
#일반 객체 ##########################################################
def val_set() :
    #     global endcode,climate,windtime,windforce,hp,dron_gps,a
    #     endcode = 0
    #     climate = 0
    #     windtime = 0
    #     windforce = 0
    #     hp = 0
    #     dron_gps = [0,0] #드론 위치(GPS)
    #     a = 0
    print('')

def dic(x):
    return l[x]

def ran_cl() :
    global climate
    #print('날씨 확인중')
    #ti.sleep(0.1)
    climate = random.randint(1,11)
    if climate <= 4 :
        climate = 'rain'
        # print('rain')
    else :
        climate = 'clean'
        # print('clean')
        
def falling(hight, m) :
    global dama,hp,endcode
    
    g = 9.8
    dama = int(m*hight * random.randint(8, 10)/10)
    # print(f'받은 충격량 {dama}')

    # try :
    #     dama = random.randint(5,hight)
    # except ValueError :
    #     dama = random.randint(hight,5)
    
    
    hp = hp - dama
    endcode = 1
    print(f'추락! 남은 내구도 : {hp}'); print(windforce); print(dron_gps[0])

def wind():
    global windforce,windtime
    # print(f'바람 시간 {windtime}')
    if windtime < 5 :
        windforce = int(random.randint(1,9))
    elif windtime < 8 :
        windforce = int(random.randint(8,13))
    elif windtime < 12 :
        windforce = int(random.randint(12,19))
    elif windtime < 15 :
        windforce = int(random.randint(18,23))
    elif windtime < 17 :
        windforce = int(random.randint(22,28))
    else : 
        windforce = int(random.randint(27,31))

    # print(f'바람 세기 {windforce}')

def parachute(env, hight) :
    global endcode,windtime
    #print(hight)
    print('낙하산')
    while True :
        hight = hight - 0.5
        wind()
        sensor = windforce/4
        windtime = windtime + 1
        if sensor >= 6 or sensor <= -6 :
            # print('senor3')
            falling(hight,m=220)
            endcode = 1
            break

        if hight <= 0 :
            # print('land with parachute')
            endcode = 1
            break

        move(v=5)
        if end_gps[0] == dron_gps[0] :
            print('목적지 도착, 물품 수령중')
            yield env.timeout(10)
            a = 1
            
        if 0 == dron_gps[0] :
            print('귀환 완료')
            a = 0
            yield env.timeout(10)
            break
               
def dron_sen_start():
    global endcode,windtime,a,done,done_2
    env = si.Environment()
    env.process(dron_sen(env))
    env.run()
    # print('.....')
    windtime = 0
    endcode = 0
    a = 0
    # val_set()
    dron_sen_hp.append(hp)
    l[2] = hp

def dron_start() :
    global endcode,windtime,a,done,done_1
    env = si.Environment()
    env.process(dron(env))
    env.run()
    windtime = 0
    endcode = 0
    a = 0
    # val_set()
    dron_hp.append(hp)
    l[1] = hp

def go(v=10):
    global end_gps,dron_gps
    # print('이동중')
    dron_gps[0] = dron_gps[0] + 10
    # print(f'남은 거리{end_gps[0] - dron_gps[0]}')

def back(v=10):
    global end_gps,dron_gps
    # print('귀환중')
    dron_gps[0] = dron_gps[0] - 10
    # print(f'남은 거리{dron_gps[0]}')

def move(v=10) :
    global a
    if a == 0 :
        go(v)
    if a == 1 :
        back(v)

#시뮬레이션 객체 ######################################################

def dron_sen(env):
    global windtime,windforce,hp,endcode,end_gps,dron_gps,a,done_2
    hight = 10 #드론 높이 
    sensor = int(0) #자이로 센서
    hp = 2200
    dron_gps = [0,0] #드론 위치(GPS)
    end_gps = [130,0] #목적지 위치
    windtime = 0

    while endcode == 0 :    
        # print(f'받은 코드 {endcode}')
        if endcode != 0 :
            break
        ran_cl()
        # print(f'날씨 {climate}')

        '''목적지까지 이동'''
        move()
        if end_gps[0] == dron_gps[0] :
            # print('목적지 도착, 물품 수령중')
            yield env.timeout(10)
            a = 1
        if 0 == dron_gps[0] :
            print('귀환 완료')
            a = 0
            done_2 = done_2 + 1
            break
        
        if climate == 'rain' :
            wind()
            # print(f'바람세기 {windforce}')
            sensor = windforce/4
            windtime = windtime + 1
            # print(f'센서 {sensor}')

            if hight == 0 :
                # print('land')
                break

            if sensor <=3 or sensor >=-3 :
                # print('senor1')
                # print('자이로센서 값 :' + str(sensor))
                hight = hight - 1
                # print(f'높이 {hight}')

            if sensor <=4 or sensor >=-4 :
                # print('senor2')
                # print('자이로센서 값 :' + str(sensor))
                parachute(env, hight)
                #print('센서값 이상')
                # print(f'높이 {hight}')

            if sensor >= 5 or sensor <= -5 :
                # print('senor3')
                falling(hight,m=220)
                endcode = 1
                break


        #ti.sleep(0.2)
        
    yield env.timeout(1)

def dron(env):
    global windtime,windforce,hp,endcode,end_gps,dron_gps,a,done_1
    end_gps = [130,0]
    hight = 10 #드론 높이
    hp = 2200
    while endcode == 0 :    
        ran_cl()
        if climate == 'rain' :
            wind()
            # print(f'바람세기  {windforce}')
            windtime = windtime + 1
            if windforce  >= 18 :
                falling(hight,m=200)
                break
        
        move()
        if end_gps[0] == dron_gps[0] :
            # print('목적지 도착, 물품 수령중')
            yield env.timeout(10)
            a = 1
            
        if 0 == dron_gps[0] :
            print('귀환 완료')
            a = 0
            done_1 = done_1 + 1
            yield env.timeout(10)
            break

        if endcode != 0 :
            break
        #ti.sleep(0.2)
        
    yield env.timeout(1)


#시뮬래이션 시작 #######################################################

print('''
상황 : 날씨가 좋지 않은날 비상착륙이 장비된 드론과 일반드론의 파손률 비교
(3초 후 시뮬레이션 시작)
''')
ti.sleep(3)

ans = int(input('반복 횟수 입력 >>>'))

for i in range(ans) :

    # ti.sleep(1)
    print('일반 드론')
    dron_start()

    # ti.sleep(1)
    print('자이로센서 탑제 드론')
    dron_sen_start()

    if not l[1] == l[2] :
        m = max(l.keys(), key=dic)
        key_M.append(m)
        m = 0

    # print(l)
    # print(m)
    # print(key_M)

    print(f'반복 횟수 : {i+1}')
    l = {}

# print(f'''
# 일반드론 추락 후 내구도 > 
# {dron_hp}
# ''')

# print(f'''
# 자이로센서 드론 추락 후 내구도 >
# {dron_sen_hp}
# ''')
frame = pd.DataFrame({
    '드론 종류 / ' : ['1번드론','2번드론'],
    '남은 내구도가 많았던 횟수 / ' : [str(key_M.count(1))+'번',str(key_M.count(2))+ '번'],
    '베달 완료 횟수 / ' : [str(done_1)+'번',str(done_2)+'번']},
    index=[1,2]
)
frame.to_excel('result.xlsx')
print(frame)
# print('결과')
# print('일반드론', str(key_M.count(1)), '번' ,'최대체력',str(max(dron_hp)), '배달 완료 횟수' , str(done_1),'번')
# print('센서 탑재 드론', str(key_M.count(2)), '번','최대체력',str(max(dron_sen_hp)), '배달 완료 횟수' , str(done_2),'번')
ans = input()