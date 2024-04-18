import os
import sqlite3
import sys

save_path = os.getcwd()
action_path = '/home/pi/TonyPi/ActionGroups'

file_list = os.listdir(action_path)
d6a_list = []
for file in file_list:
    if os.path.splitext(file)[1] == '.d6a':
        d6a_list.append(file)
    
for f in d6a_list:    
    a_g = []
    print(os.path.join(action_path, f))
    ag = sqlite3.connect(os.path.join(action_path, f))
    cu = ag.cursor()
    cu.execute("select * from ActionGroup")
    while True:
        act = cu.fetchone()
        if act is not None:
            act_group = []
            act_group.append(act[1]) 
            for i in range(0, len(act) - 2, 1):
                act_group.append(act[2 + i])
            act_group.append(500)
            act_group.append(500)
            a_g.append(act_group)
        else:   # 运行完才退出
            break    
        
    cu.close()
    ag.close()

    conn = sqlite3.connect(os.path.splitext(os.path.join(save_path, f))[0]+".d6a")
    c = conn.cursor()
    c.execute('''CREATE TABLE ActionGroup([Index] INTEGER PRIMARY KEY AUTOINCREMENT
    NOT NULL ON CONFLICT FAIL
    UNIQUE ON CONFLICT ABORT,
    Time INT,
    Servo1 INT,
    Servo2 INT,
    Servo3 INT,
    Servo4 INT,
    Servo5 INT,
    Servo6 INT,
    Servo7 INT,
    Servo8 INT,
    Servo9 INT,
    Servo10 INT,
    Servo11 INT,
    Servo12 INT,
    Servo13 INT,
    Servo14 INT,
    Servo15 INT,
    Servo16 INT,
    Servo17 INT,
    Servo18 INT);''')

    for dat in a_g:
        str1 = "INSERT INTO ActionGroup(Time, Servo1, Servo2, Servo3, Servo4, Servo5," \
               " Servo6, Servo7,  Servo8, Servo9,  Servo10, Servo11,  Servo12, Servo13,  " \
               "Servo14, Servo15,  Servo16, Servo17,  Servo18) "
        str2 = "VALUES("
        for i in range(0, 18):
            str2 += str(dat[i]) + ','
        str2 += str(dat[18])
        str1 = str1 + str2 + ");"
        print(str1)
        c.execute(str1)
    print("\n\n")
    conn.commit()
    conn.close()