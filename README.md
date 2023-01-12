# 電流吉吉棒
- 原名: Listen, Watch, Run
---
tags: LSA
---

# 電流吉吉棒
[TOC]
- 原名: Listen, Watch, Run


## 實作念想 
- 動機 : 
    - 中漢覺得吉娃娃面目可憎很討厭, 所以我們決定要讓它通過一連串的考驗, 我們設置了一段賽道, 賽道會有不同的電流, 當她碰到賽道就會被電擊, 當他被不同的電擊就會發出不同叫聲, 我們覺得他很吵, 所以需要大家協助這隻吉娃娃走過這個賽道, 讓他不要吉吉叫！科科
- 功能 :
    - 地圖顏色偵測
    - 採到顏色車子會發出不同音效
        -  紅(終點線) : 音效 [Century YEE](https://www.youtube.com/watch?v=OTk6m3U54po&ab_channel=KUSHLORD)
        -  綠 : 音效 [TADAAH](https://www.youtube.com/watch?v=jLtbFWJm9_M&list=PLen20o33zLu53DXEZDy53UKH9CHknSMld&index=35&ab_channel=GamingSoundFX)
        -  藍 : 音效 [HOT HOT HOT](https://www.youtube.com/watch?v=vFrNxJoB768&list=PLen20o33zLu53DXEZDy53UKH9CHknSMld&index=40&ab_channel=GamingSoundFX)
        -  黃 : 音效 [YEE](https://www.youtube.com/watch?v=q6EoRBvdVPQ&ab_channel=revergo)
    - 網頁控制開始紀錄時間與結束時紀錄到網頁
    - 記錄好每次的時間後進行排名, 時間越短名次越前面(數字越小)


## 硬體設備
| 設備名稱        |                  圖片網址                    |        來源          |
|----------------|--------------------------------------------|----------------------|
| Raspberry Pi 4 | <img src="https://i.imgur.com/BEZPftv.jpg" width="30%x"> | 友情贊助(石安通學長提供) |
| mbot車         | <img src="https://i.imgur.com/KK7WuRG.jpg" width="30%x"> | 友情贊助(林宜蔓學姊提供) |
| 藍芽喇叭        | <img src="https://i.imgur.com/2W7WH8T.jpg" width="30%x">|     張中漢提供          |
| 杜邦線n         | <img src="https://i.imgur.com/6GoIwi3.jpg" width="30%x"> | 友情贊助(朋友*n)        |
| ~~Arduino~~    | <img src="https://i.imgur.com/xTBTYco.jpg" width="30%x"> | 友情提供(張中漢同學)    |
| 顏色感測器       | <img src="https://i.imgur.com/QJ597Ex.jpg" width="30%x"> | 蝦皮                |


## 安裝設定過程
#### GPIO & 設備
![](https://i.imgur.com/cEbRA4x.png)

#### 顏色感測器 TCS34725
| 顏色感測器接口 | raspberry pi接口 |
|--------------|-----------------|
|     VIN      |        5V       |
|     GND      |        GND      |
|     SCL      |        A5       |
|     SDA      |        A4       |

> 安裝adafruit library
```
sudo pip3 install adafruit-circuitpython-tcs34725
```
> 修改設定檔 (開啟I2C的通訊協定)
```
sudo raspi-config 
//重新啟動
sudo reboot
```

> 安裝wiringPi (可控制GPIO的函數庫)
```
sudo apt-get install wiringpi
wget https://project-downloads.drogon.net/wiringpi-latest.deb
sudo dpkg -i wiringpi-latest.deb
gpio -v
```

> WebSocket
```python=
async def sendCmd(uri, msg):
    async with websockets.connect(uri) as websockets:
        await websocket.send(msg)
```


## car photo & 成果影片
影片一
https://youtube.com/shorts/ixodvznrxMY?feature=share

影片二
https://youtube.com/shorts/F6QM63x0BYs?feature=share

影片三 (最終成果)
https://www.youtube.com/watch?v=GDMttdhcqYo&ab_channel=ZoeyChien


## Programing
### Car (mbot用來行走)
* mbot 可以兼容 arduino
* 導入相關套件
```C++=
// generated by mBlock5 for mBot
// codes make you happy

#include <MeMCore.h>
#include <Arduino.h>
#include <Wire.h>
#include <SoftwareSerial.h>
```

* 設定紅外線遙控與馬達
```C++=
MeIR ir;
MeDCMotor motor_9(9);
MeDCMotor motor_10(10);
```

* 設定馬達在前後左右的方向
```C++=
void move(int direction, int speed) {
    int leftSpeed = 0;
    int rightSpeed = 0;
    if(direction == 1) {
        leftSpeed = speed;
        rightSpeed = speed;
    } else if(direction == 2) {
        leftSpeed = -speed;
        rightSpeed = -speed;
    } else if(direction == 3) {
        leftSpeed = -speed;
        rightSpeed = speed;
    } else if(direction == 4) {
        leftSpeed = speed;
        rightSpeed = -speed;
    }
    motor_9.run((9) == M1 ? -(leftSpeed) : (leftSpeed));
    motor_10.run((10) == M1 ? -(rightSpeed) : (rightSpeed));
}

void _delay(float seconds) {
    long endTime = millis() + seconds * 1000;
    while(millis() < endTime) _loop();
}
```

* 設定遙控時，前進左右的馬達運動速度
```C++=
void setup() {
    ir.begin();
    while(1) {
        if(ir.keyPressed(64)){
            move(2, 40 / 100.0 * 255);  
            _delay(0.1);
            move(2, 0);
        }
        if(ir.keyPressed(25)){
            move(1, 40 / 100.0 * 255);
            _delay(0.1);
            move(1, 0);
        }
        if(ir.keyPressed(7)){
            move(3, 30 / 100.0 * 255);
            _delay(0.1);
            move(3, 0);
        }
        if(ir.keyPressed(9)){
            move(4, 30 / 100.0 * 255);
            _delay(0.1);
            move(4, 0);
        }
        _loop();
   }
}
```

* 需持續偵測紅外線遙控訊號
```C++=
void _loop() {
    ir.loop();
}

void loop() {
    _loop();
}
```


## Usage
- 步驟 : 
    1. 在Ubuntu上執行 server.py
    2. 重整網頁
    3. 在樹莓派上執行以寫到裡面的程式 car.py 


## Job Assignment
|    組員    |               工作分配              |
|-----------|------------------------------------|
| **全部人** |     **硬體組裝, 程式, 地圖, 跑腿**     |
| 張中漢     | 設備場地, 車車程式, 焊接, 食物提供, 報告 |
| 簡語萱     |   程式, github, web connect, ppt    |
| 陳思妤     |    程式, github, web server, ppt    |
| 陳煒姍     |     程式, github, web page, ppt     |
| 吳常恩     |             測試, 報告               |


## References
> - 顏色感測器
> [1. TCS3200顏色感測器模組(TCS230升級版)](https://www.icshop.com.tw/product-page.php?9486)
> - 樹梅派連接arduino
> https://s761111.gitbook.io/raspi-sensor/pai-arduino
> - 樹莓派連接顏色感測器
> https://learn.adafruit.com/adafruit-color-sensors/python-circuitpython


## Future
- 將車身換掉(第2台)
    - 可操控輪子馬達做聲音辨識控制車子移動
    - 車子身上之webcam紀錄移動軌跡到網頁上
    - ![](https://i.imgur.com/MSh2zZq.jpg)


## thank you ♡♡
- 安通學長 : 器材提供
- 惠霖學姊 : 溫柔大姊姊debug
- 宜蔓學姊 : 提供mbot車身
- 簡先生 : websocket教學
- 柏瑋學長 : 思考方向提供


## 簡報
https://www.canva.com/design/DAFWsbh7i_I/sOb-uMQBgqB8cr_T3EKsDw/edit?utm_content=DAFWsbh7i_I&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

