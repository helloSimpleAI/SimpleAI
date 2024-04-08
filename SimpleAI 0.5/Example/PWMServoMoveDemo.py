import time
import hiwonder.Board as Board

print('''
**********************************************************
********功能:幻尔科技TonyPi扩展板，PWM舵机控制例程********
**********************************************************
----------------------------------------------------------
Official website:http://www.hiwonder.com
Online mall:https://huaner.tmall.com/
----------------------------------------------------------
以下指令均需在LX终端使用，LX终端可通过ctrl+alt+t打开，或点
击上栏的黑色LX终端图标。
----------------------------------------------------------
Usage:
    python3 BusServoMove.py
----------------------------------------------------------
Version: --V1.2  2021/07/03
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！
----------------------------------------------------------
''')

while True:
    # 参数：参数1：舵机接口编号; 参数2：位置; 参数3：运行时间
    Board.setPWMServoPulse(2, 1500, 500) # 2号舵机转到1500位置，用时500ms
    time.sleep(0.5) # 延时时间和运行时间相同
    
    Board.setPWMServoPulse(2, 1800, 500) #舵机的转动范围0-180度，对应的脉宽为500-2500,即参数2的范围为500-2500
    time.sleep(0.5)
    
    Board.setPWMServoPulse(2, 1500, 200)
    time.sleep(0.2)
    
    Board.setPWMServoPulse(2, 1800, 500)  
    Board.setPWMServoPulse(1, 1800, 500)
    time.sleep(0.5)
    
    Board.setPWMServoPulse(2, 1500, 500)  
    Board.setPWMServoPulse(1, 1500, 500)
    time.sleep(0.5)    