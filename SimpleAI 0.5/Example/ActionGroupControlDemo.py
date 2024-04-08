import time
import threading
import hiwonder.ActionGroupControl as AGC

print('''
**********************************************************
*********功能:幻尔科技TonyPi扩展板，动作组控制例程********
**********************************************************
----------------------------------------------------------
Official website:http://www.hiwonder.com
Online mall:https://huaner.tmall.com/
----------------------------------------------------------
以下指令均需在LX终端使用，LX终端可通过ctrl+alt+t打开，或点
击上栏的黑色LX终端图标。
----------------------------------------------------------
Usage:
    python3 ActionGroupControlDemo.py
----------------------------------------------------------
Version: --V1.2  2021/07/03
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！
----------------------------------------------------------
''')

# 动作组需要保存在路径/home/pi/TonyPi/ActionGroups下
AGC.runActionGroup('stand')  # 参数为动作组的名称，不包含后缀，以字符形式传入
AGC.runActionGroup('go_forward', times=2, with_stand=True)  # 第二个参数为运行动作次数，默认1, 当为0时表示循环运行， 第三个参数表示最后是否以立正姿态收步

threading.Thread(target=AGC.runActionGroup, args=('go_forward', 0, True)).start()  # 运行动作函数是阻塞式的，如果要循环运行一段时间后停止，请用线程来开启
time.sleep(3)
AGC.stopActionGroup()  # 前进3秒后停止