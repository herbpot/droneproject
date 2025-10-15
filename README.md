# droneproject

Arduino 기반 드론 제어 및 배터리 충전 방식 비교 시뮬레이션 프로젝트입니다.

## 개요

droneproject는 Arduino와 MPU6050 센서를 사용한 드론 하드웨어 제어와 Python simpy를 이용한 배터리 성능 시뮬레이션을 결합한 프로젝트입니다. 일반 배터리, 레이저 무선충전, 태양광 충전 등 3가지 충전 방식의 드론 비행 시간을 비교 분석합니다.

## 주요 기능

### 하드웨어 (Arduino)
- **MPU6050 센서**: 3축 가속도계 + 3축 자이로스코프
- **블루투스 제어**: 시리얼 통신으로 드론 제어
- **모터 제어**: 상승/하강/정지 명령
- **실시간 각도 측정**: X, Y, Z축 각도 데이터 전송

### 시뮬레이션 (Python)
- **배터리 시뮬레이션**: SimPy를 이용한 이산 사건 시뮬레이션
- **3가지 충전 방식 비교**: 일반 vs 레이저 vs 태양광
- **비행 거리 계산**: 배터리 수명에 따른 이동 거리
- **통계 분석**: pandas와 Excel로 결과 출력
- **제한 구역 시뮬레이션**: 비행 금지 구역 회피

## 기술 스택

### 하드웨어
- **Arduino** - 마이크로컨트롤러
- **MPU6050** - 6축 관성 센서
- **HC-06/05** - 블루투스 모듈
- **L298N** - 모터 드라이버

### 소프트웨어
- **Arduino C++** - 펌웨어
- **Python 3.x** - 시뮬레이션
- **SimPy** - 이산 사건 시뮬레이션
- **pandas** - 데이터 분석
- **numpy** - 수치 계산

## 프로젝트 구조

```
droneproject/
├── dron_project.ino                # Arduino 펌웨어
├── simmulate_battery.py            # 배터리 비교 시뮬레이션
├── simmulate_flying.py             # 비행 시뮬레이션
├── simmulate_restricted_area.py    # 제한 구역 시뮬레이션
├── simmulate_going.py              # 이동 시뮬레이션
├── simtest.py                      # 테스트 스크립트
├── drone/                          # 드론 관련 파일
├── wifi/                           # WiFi 모듈 관련
├── result.xlsx                     # 시뮬레이션 결과
├── result_1.xlsx
├── result_1_battery.xlsx
└── result_1_flying.xlsx
```

## 하드웨어 구성

### 회로 연결

```
Arduino Uno
├── MPU6050 (I2C)
│   ├── VCC → 5V
│   ├── GND → GND
│   ├── SDA → A4
│   └── SCL → A5
├── 블루투스 모듈 (HC-06)
│   ├── VCC → 5V
│   ├── GND → GND
│   ├── TX → Pin 2
│   └── RX → Pin 3
└── 모터 드라이버 (L298N)
    ├── IN1 → Pin 9
    └── IN2 → Pin 6
```

## 설치 및 실행

### Arduino 설정

1. **라이브러리 설치**
   - Arduino IDE 실행
   - 스케치 → 라이브러리 포함 → 라이브러리 관리
   - 검색 및 설치:
     - `MPU6050_tockn`
     - `Wire`
     - `SoftwareSerial`

2. **펌웨어 업로드**
```arduino
1. dron_project.ino 열기
2. 보드: Arduino Uno 선택
3. 포트 선택
4. 업로드 버튼 클릭
```

### Python 설정

```bash
pip install simpy numpy pandas openpyxl
```

## 사용 방법

### 1. 드론 제어 (블루투스)

**명령어:**
- `1` - 상승 (1초간)
- `2` - 하강 (1초간)
- `3` - 정지

**각도 데이터 수신:**
```
angleX : 12.34  angleY : 56.78  angleZ : 90.12
```

### 2. 배터리 시뮬레이션 실행

```bash
python simmulate_battery.py
반복횟수 입력 >>> 100
```

**시뮬레이션 설정:**
- **드론 1 (일반 배터리)**
  - 용량: 3100 mAh (620 × 5)
  - 소비: 11500 mA (2300 × 5)
  - 비행 시간: ~16분

- **드론 2 (레이저 충전)**
  - 용량: 3100 mAh
  - 소비: 11500 mA
  - 충전: 45 mA/분 (지속)
  - 비행 시간: 증가

- **드론 3 (태양광 충전)**
  - 용량: 3000 mAh
  - 소비: 11500 mA
  - 충전: 0.15~0.35 mA (가변)
  - 비행 시간: 날씨 의존

**출력 예시 (result.xlsx):**

| 드론 종류 | 가장 오래간 횟수 |
|-----------|-----------------|
| 1번드론 (일반) | 5번 |
| 2번드론 (레이저) | 85번 |
| 3번드론 (태양광) | 10번 |

## 핵심 코드 구현

### Arduino - MPU6050 데이터 읽기

```cpp
#include <MPU6050_tockn.h>
#include <Wire.h>

MPU6050 mpu(Wire);

void setup() {
  mpu.begin();
  mpu.calcGyroOffsets(true);
  Serial.begin(9600);
  Wire.begin();
}

void loop() {
  mpu.update();
  mySerial.print("angleX : ");
  mySerial.print(mpu.getAngleX());
  mySerial.print("\tangleY : ");
  mySerial.print(mpu.getAngleY());
  mySerial.print("\tangleZ : ");
  mySerial.println(mpu.getAngleZ());
  delay(1000);
}
```

### Arduino - 블루투스 모터 제어

```cpp
if (mySerial.available()){
  char read1;
  read1 = mySerial.read();

  if(read1 == '1'){
    digitalWrite(6, HIGH);
    digitalWrite(9, LOW);  // 상승
    delay(1000);
  }
  else if(read1 == '2'){
    digitalWrite(6, LOW);
    digitalWrite(9, HIGH);  // 하강
    delay(1000);
  }
  else if(read1 == '3') {
    digitalWrite(6, LOW);
    digitalWrite(9, LOW);  // 정지
    delay(1000);
  }
}
```

### Python - 일반 배터리 드론

```python
def dron_1(env):
    global battery_1, dron_gps_1
    battery_1 = 620 * 5  # 3100 mAh
    dron_gps_1 = [0, 0]
    use_b_1 = 2300 * 5  # 소비량
    timer_1 = battery_1 / use_b_1 * 60  # 비행 시간(분)

    while timer_1 > 1:
        timer_1 = timer_1 - 1
        dron_gps_1[0] = dron_gps_1[0] + 10  # 10m 이동
        yield env.timeout(1)
```

### Python - 레이저 충전 드론

```python
def dron_2(env):
    global battery_2, dron_gps_2
    battery_2 = 620 * 5
    dron_gps_2 = [0, 0]
    use_b_2 = 2300 * 5
    timer_2 = battery_2 / use_b_2 * 60
    charge_t_1 = 45 / use_b_2 * 60  # 충전량

    while timer_2 > 1:
        timer_2 = timer_2 - 1
        timer_2 = timer_2 + charge_t_1  # 지속 충전
        dron_gps_2[0] = dron_gps_2[0] + 10
        yield env.timeout(1)
```

### Python - 태양광 충전 드론

```python
def dron_3(env):
    global battery_3, dron_gps_3
    battery_3 = 600 * 5
    use_b_3 = 2300 * 5
    charge_t_3 = np.random.randint(3, 7) / 10 * 0.5  # 랜덤 충전
    timer_3 = (battery_3 + charge_t_3) / use_b_3 * 60

    while timer_3 > 1:
        timer_3 = timer_3 - 1
        timer_3 = timer_3 + charge_t_3  # 가변 충전
        dron_gps_3[0] = dron_gps_3[0] + 10
        yield env.timeout(1)
```

### Python - 결과 저장

```python
frame = pd.DataFrame({
    '드론 종류 / ': ['1번드론', '2번드론', '3번드론'],
    '가장 오래간 횟수 / ': [
        str(key_M.count('1번')) + '번',
        str(key_M.count('2번')) + '번',
        str(key_M.count('3번')) + '번'
    ]
}, index=[1, 2, 3])
frame.to_excel('result.xlsx')
print(frame)
```

## 시뮬레이션 결과 분석

### 가정

- 태양광 사용 불가능한 날은 날씨가 나빠 드론 운행도 불가능하므로 제외
- 모든 드론은 동일한 속도(10m/분)로 이동
- 레이저 충전은 거리에 따른 효율 감소 없음

### 예상 결과

**100회 시뮬레이션 기준:**
- 1번 드론 (일반): 약 5-10회 우승
- 2번 드론 (레이저): 약 80-90회 우승 ⭐
- 3번 드론 (태양광): 약 5-10회 우승

**결론:** 레이저 무선충전 방식이 가장 효율적

## 하드웨어 확장

### 추가 센서

```cpp
// 초음파 센서 (장애물 감지)
#define TRIG_PIN 7
#define ECHO_PIN 8

long distance = measureDistance();

long measureDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  return duration * 0.034 / 2;
}
```

### GPS 모듈

```cpp
#include <TinyGPS++.h>
#include <SoftwareSerial.h>

TinyGPSPlus gps;
SoftwareSerial gpsSerial(10, 11);

void loop() {
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
    if (gps.location.isUpdated()) {
      Serial.print("Lat: ");
      Serial.print(gps.location.lat(), 6);
      Serial.print(" Lng: ");
      Serial.println(gps.location.lng(), 6);
    }
  }
}
```

## 트러블슈팅

### MPU6050 초기화 실패

```
MPU6050 connection failed
```

해결:
- I2C 연결 확인 (SDA=A4, SCL=A5)
- 풀업 저항 확인 (4.7kΩ)
- 주소 확인 (0x68 또는 0x69)

### 블루투스 연결 안 됨

- HC-06 기본 페어링 코드: 1234 또는 0000
- Baud rate: 9600

### 시뮬레이션 느림

```python
# 출력 제거로 속도 향상
# print() 문을 주석 처리
```

## 향후 계획

- [ ] 실제 하드웨어 드론 제작
- [ ] PID 제어 알고리즘 구현
- [ ] 자율 비행 (GPS 기반)
- [ ] 카메라 스트리밍
- [ ] 앱으로 제어 (MIT App Inventor)
- [ ] 배터리 충전 하드웨어 실험
- [ ] 드론 편대 비행 시뮬레이션

## 참고 자료

- [MPU6050 데이터시트](https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/)
- [SimPy 문서](https://simpy.readthedocs.io/)
- [Arduino 블루투스 튜토리얼](https://www.arduino.cc/en/Guide/ArduinoBT)

## 라이선스

교육 목적으로 작성된 프로젝트입니다.
