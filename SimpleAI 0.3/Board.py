#!/usr/bin/env python3
import os
import sys
import time
import pigpio
import RPi.GPIO as GPIO
from . import PWMServo
from . import BusServoCmd
from smbus2 import SMBus, i2c_msg

#幻尔科技TonyPi扩展板sdk#
if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

Servos = ()
pi = pigpio.pi()
def initPWMServo(d):
    global Servos
    
    servo1 = PWMServo.PWM_Servo(pi, 12, deviation=d[0], control_speed=True)  # 扩展板上的1
    servo2 = PWMServo.PWM_Servo(pi, 13, deviation=d[1], control_speed=True)  # 2
    Servos = (servo1, servo2)

d = [0, 0]
initPWMServo(d)

def setPWMServoPulse(servo_id, pulse = 1500, use_time = 1000):
    if servo_id < 1 or servo_id > 2:
        return

    pulse = 2500 if pulse > 2500 else pulse    
    pulse = 500 if pulse < 500 else pulse 
    use_time = 30000 if use_time > 30000 else use_time    
    use_time = 20 if use_time < 20 else use_time

    Servos[servo_id - 1].setPosition(pulse, use_time)

    return pulse

def setDeviation(servo_id, dev):
    if servo_id < 1 or servo_id > 2:
        return
    if d < -300 or d > 300:
        return
    Servos[servo_id - 1].setDeviation(dev)

def setBuzzer(new_state):
    GPIO.setup(31, GPIO.OUT)
    GPIO.output(31, new_state)

def setBusServoID(oldid, newid):
    """
    配置舵机id号, 出厂默认为1
    :param oldid: 原来的id， 出厂默认为1
    :param newid: 新的id
    """
    BusServoCmd.serial_servo_wirte_cmd(oldid, BusServoCmd.LOBOT_SERVO_ID_WRITE, newid)

def getBusServoID(id=None):
    """
    读取串口舵机id
    :param id: 默认为空
    :return: 返回舵机id
    """
    
    while True:
        if id is None:  # 总线上只能有一个舵机
            BusServoCmd.serial_servo_read_cmd(0xfe, BusServoCmd.LOBOT_SERVO_ID_READ)
        else:
            BusServoCmd.serial_servo_read_cmd(id, BusServoCmd.LOBOT_SERVO_ID_READ)
        # 获取内容
        msg = BusServoCmd.serial_servo_get_rmsg(BusServoCmd.LOBOT_SERVO_ID_READ)
        if msg is not None:
            return msg

def setBusServoPulse(id, pulse, use_time):
    """
    驱动串口舵机转到指定位置
    :param id: 要驱动的舵机id
    :pulse: 位置
    :use_time: 转动需要的时间
    """

    pulse = 0 if pulse < 0 else pulse
    pulse = 1000 if pulse > 1000 else pulse
    use_time = 0 if use_time < 0 else use_time
    use_time = 30000 if use_time > 30000 else use_time
    BusServoCmd.serial_servo_wirte_cmd(id, BusServoCmd.LOBOT_SERVO_MOVE_TIME_WRITE, pulse, use_time)

def stopBusServo(id=None):
    '''
    停止舵机运行
    :param id:
    :return:
    '''
    BusServoCmd.serial_servo_wirte_cmd(id, BusServoCmd.LOBOT_SERVO_MOVE_STOP)

def setBusServoDeviation(id, d=0):
    """
    调整偏差
    :param id: 舵机id
    :param d:  偏差
    """
    BusServoCmd.serial_servo_wirte_cmd(id, BusServoCmd.LOBOT_SERVO_ANGLE_OFFSET_ADJUST, d)

def saveBusServoDeviation(id):
    """
    配置偏差，掉电保护
    :param id: 舵机id
    """
    BusServoCmd.serial_servo_wirte_cmd(id, BusServoCmd.LOBOT_SERVO_ANGLE_OFFSET_WRITE)

time_out = 200
def getBusServoDeviation(id):
    '''
    读取偏差值
    :param id: 舵机号
    :return:
    '''
    # 发送读取偏差指令
    count = 0
    while True:
        BusServoCmd.serial_servo_read_cmd(id, BusServoCmd.LOBOT_SERVO_ANGLE_OFFSET_READ)
        # 获取
        msg = BusServoCmd.serial_servo_get_rmsg(BusServoCmd.LOBOT_SERVO_ANGLE_OFFSET_READ)
        count += 1
        if msg is not None:
            return msg
        if count > time_out:
            return None

def setBusServoAngleLimit(id, low, high):
    '''
    设置舵机转动范围
    :param id:
    :param low:
    :param high:
    :return:
    '''
    BusServoCmd.serial_servo_wirte_cmd(id, BusServoCmd.LOBOT_SERVO_ANGLE_LIMIT_WRITE, low, high)

def getBusServoAngleLimit(id):
    '''
    读取舵机转动范围
    :param id:
    :return: 返回元祖 0： 低位  1： 高位
    '''
    
    while True:
        BusServoCmd.serial_servo_read_cmd(id, BusServoCmd.LOBOT_SERVO_ANGLE_LIMIT_READ)
        msg = BusServoCmd.serial_servo_get_rmsg(BusServoCmd.LOBOT_SERVO_ANGLE_LIMIT_READ)
        if msg is not None:
            count = 0
            return msg

def setBusServoVinLimit(id, low, high):
    '''
    设置舵机电压范围
    :param id:
    :param low:
    :param high:
    :return:
    '''
    BusServoCmd.serial_servo_wirte_cmd(id, BusServoCmd.LOBOT_SERVO_VIN_LIMIT_WRITE, low, high)

def getBusServoVinLimit(id):
    '''
    读取舵机转动范围
    :param id:
    :return: 返回元祖 0： 低位  1： 高位
    '''
    while True:
        BusServoCmd.serial_servo_read_cmd(id, BusServoCmd.LOBOT_SERVO_VIN_LIMIT_READ)
        msg = BusServoCmd.serial_servo_get_rmsg(BusServoCmd.LOBOT_SERVO_VIN_LIMIT_READ)
        if msg is not None:
            return msg

def setBusServoMaxTemp(id, m_temp):
    '''
    设置舵机最高温度报警
    :param id:
    :param m_temp:
    :return:
    '''
    BusServoCmd.serial_servo_wirte_cmd(id, BusServoCmd.LOBOT_SERVO_TEMP_MAX_LIMIT_WRITE, m_temp)

def getBusServoTempLimit(id):
    '''
    读取舵机温度报警范围
    :param id:
    :return:
    '''
    
    while True:
        BusServoCmd.serial_servo_read_cmd(id, BusServoCmd.LOBOT_SERVO_TEMP_MAX_LIMIT_READ)
        msg = BusServoCmd.serial_servo_get_rmsg(BusServoCmd.LOBOT_SERVO_TEMP_MAX_LIMIT_READ)
        if msg is not None:
            return msg

def getBusServoPulse(id):
    '''
    读取舵机当前位置
    :param id:
    :return:
    '''
    while True:
        BusServoCmd.serial_servo_read_cmd(id, BusServoCmd.LOBOT_SERVO_POS_READ)
        msg = BusServoCmd.serial_servo_get_rmsg(BusServoCmd.LOBOT_SERVO_POS_READ)
        if msg is not None:
            return msg

def getBusServoTemp(id):
    '''
    读取舵机温度
    :param id:
    :return:
    '''
    while True:
        BusServoCmd.serial_servo_read_cmd(id, BusServoCmd.LOBOT_SERVO_TEMP_READ)
        msg = BusServoCmd.serial_servo_get_rmsg(BusServoCmd.LOBOT_SERVO_TEMP_READ)
        if msg is not None:
            return msg

def getBusServoVin(id):
    '''
    读取舵机电压
    :param id:
    :return:
    '''
    while True:
        BusServoCmd.serial_servo_read_cmd(id, BusServoCmd.LOBOT_SERVO_VIN_READ)
        msg = BusServoCmd.serial_servo_get_rmsg(BusServoCmd.LOBOT_SERVO_VIN_READ)
        if msg is not None:
            return msg

def restBusServoPulse(oldid):
    # 舵机清零偏差和P值中位（500）
    BusServoCmd.serial_servo_set_deviation(oldid, 0)    # 清零偏差
    time.sleep(0.1)
    BusServoCmd.serial_servo_wirte_cmd(oldid, BusServoCmd.LOBOT_SERVO_MOVE_TIME_WRITE, 500, 100)    # 中位

##掉电
def unloadBusServo(id):
    BusServoCmd.serial_servo_wirte_cmd(id, BusServoCmd.LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE, 0)

##读取是否掉电
def getBusServoLoadStatus(id):
    while True:
        BusServoCmd.serial_servo_read_cmd(id, BusServoCmd.LOBOT_SERVO_LOAD_OR_UNLOAD_READ)
        msg = BusServoCmd.serial_servo_get_rmsg(BusServoCmd.LOBOT_SERVO_LOAD_OR_UNLOAD_READ)
        if msg is not None:
            return msg

setBuzzer(0)
