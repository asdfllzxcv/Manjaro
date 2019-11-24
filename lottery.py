import random
import threading
import time
import tkinter
from tkinter import messagebox

import numpy as np
import pygame
import pymysql
import pymysql.cursors
from PIL import ImageTk, Image

'''
年会抽奖系统
'''

# 初始化窗口
root = tkinter.Tk()
root.title("国华人寿呼叫中心（荆门）年会晚宴抽奖活动")
root.geometry('1360x700+400+200')  # 定义界面大小
root.resizable(False, False)
root.flag = True
# 添加背景图片
canvas = tkinter.Canvas(root,
                        width=1360,
                        height=700,
                        bg='white')
image = Image.open("guohualife_gaitubao_1360x700.jpg")
im = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor='nw', image=im)  # 使用create_image将图片添加到Canvas组件中
canvas.pack()

# 全局变量的定义
award_level = 0
award_time = 0
old_data = []
# 定义抽奖调动的Label标签
first = tkinter.Label(root, text='', bg='yellow', font=('微软雅黑', 16, 'normal'))
first.place(x=150, y=200, width=90, height=50)
second = tkinter.Label(root, text='', bg='yellow', font=('微软雅黑', 16, 'normal'))
second.place(x=260, y=200, width=90, height=50)
third = tkinter.Label(root, text='', bg='yellow', font=('微软雅黑', 16, 'normal'))
third.place(x=370, y=200, width=90, height=50)
fourth = tkinter.Label(root, text='', bg='yellow', font=('微软雅黑', 16, 'normal'))
fourth.place(x=480, y=200, width=90, height=50)
fifth = tkinter.Label(root, text='', bg='yellow', font=('微软雅黑', 16, 'normal'))
fifth.place(x=590, y=200, width=90, height=50)
sixth = tkinter.Label(root, text='', bg='yellow', font=('微软雅黑', 16, 'normal'))
sixth.place(x=700, y=200, width=90, height=50)
seventh = tkinter.Label(root, text='', bg='yellow', font=('微软雅黑', 16, 'normal'))
seventh.place(x=810, y=200, width=90, height=50)
eighth = tkinter.Label(root, text='', bg='yellow', font=('微软雅黑', 16, 'normal'))
eighth.place(x=920, y=200, width=90, height=50)
ninth = tkinter.Label(root, text='', bg='yellow', font=('微软雅黑', 16, 'normal'))
ninth.place(x=1030, y=200, width=90, height=50)
tenth = tkinter.Label(root, text='', bg='yellow', font=('微软雅黑', 16, 'normal'))
tenth.place(x=1140, y=200, width=90, height=50)
# 创建显示轮次中奖名单的listbox
Listbox = tkinter.Listbox(root, bg='yellow', font=('微软雅黑', 16, 'normal'))
Listbox.place(x=100, y=300, width=900, height=300)
yscrollbar = tkinter.Scrollbar(Listbox, command=Listbox.yview)  # 给listbox加上Scrollbar滚动条
yscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
Listbox.config(yscrollcommand=yscrollbar.set)
# 创建显示中奖人数合计的listbox
Listbox_num = tkinter.Listbox(root, bg='yellow', font=('微软雅黑', 16, 'normal'))
Listbox_num.place(x=1060, y=300, width=200, height=300)
yscrollbar_num = tkinter.Scrollbar(Listbox_num, command=Listbox_num.yview)  # 给listbox加上Scrollbar滚动条
yscrollbar_num.pack(side=tkinter.RIGHT, fill=tkinter.Y)
Listbox_num.config(yscrollcommand=yscrollbar_num.set)


def awwrd_time1():
    global award_time
    award_time = '                          第一轮中奖结果'
    tkinter.messagebox.showinfo(title='消息提示', message='第一轮抽奖马上开始，祝大家好运！')
    Listbox.insert(tkinter.END, award_time)
    btnStart1.configure(state='disabled')
    btnStart2.configure(state='normal')
    btnlevel1.configure(state='normal')
    btnlevel2.configure(state='normal')
    btnlevel3.configure(state='normal')
    btnlevel4.configure(state='normal')
    btnlevel5.configure(state='normal')
    btnlevel6.configure(state='normal')


btnStart1 = tkinter.Button(root, text='第一轮', border='5', fg='white', bg='tomato',
                           font=('微软雅黑', 20, 'bold', 'normal'), command=awwrd_time1)
btnStart1.place(x=200, y=100, width=170, height=40)


def awwrd_time2():
    global award_time
    award_time = '                          第二轮中奖结果'
    tkinter.messagebox.showinfo(title='消息提示', message='第三轮抽奖马上开始，祝大家好运！')
    Listbox.insert(tkinter.END, award_time)
    btnStart2.configure(state='disabled')
    btnStart3.configure(state='normal')


btnStart2 = tkinter.Button(root, text='第二轮', border='5', fg='white', bg='tomato',
                           font=('微软雅黑', 20, 'normal'), command=awwrd_time2)
btnStart2.place(x=400, y=100, width=170, height=40)


def awwrd_time3():
    global award_time
    award_time = '                          第三轮中奖结果'
    tkinter.messagebox.showinfo(title='消息提示', message='第三轮抽奖马上开始，祝大家好运！')
    Listbox.insert(tkinter.END, award_time)
    btnStart3.configure(state='disabeld')


btnStart3 = tkinter.Button(root, text='第三轮', border='5', fg='white', bg='tomato',
                           font=('微软雅黑', 20, 'normal'), command=awwrd_time2)
btnStart3.place(x=600, y=100, width=170, height=40)

butQueryClick = tkinter.Label(root, text='轮次中奖名单如下', bg='red', font=('微软雅黑', 20, 'normal'))
butQueryClick.place(x=100, y=250, width=900, height=40)
butQueryNumClick = tkinter.Label(root, text='中奖人数汇总', bg='red', font=('微软雅黑', 20, 'normal'))
butQueryNumClick.place(x=1060, y=250, width=200, height=40)


def my_conn_select(sql):
    coon = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='xmrcw', charset='utf8')
    cur = coon.cursor()
    cur.execute(sql)
    if sql.strip()[:6] == 'SELECT':
        res = cur.fetchall()
    else:
        coon.commit()
        res = 'ok'
    cur.close()
    coon.close()
    return res


def my_conn_update(sql, data):
    coon = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='xmrcw', charset='utf8')
    cur = coon.cursor()
    cur.execute(sql, data)
    if sql.strip()[:6] == 'SELECT':
        res = cur.fetchall()
    else:
        coon.commit()
        res = 'ok'
    cur.close()
    coon.close()
    return res


class myThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(myThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()
        self.award_level = 0

    def switch(self):
        root.flag = True
        employee_sql = "SELECT name FROM employee WHERE flag='未中奖' "
        employee = my_conn_select(employee_sql)
        # print(employee)
        if len(employee) == 0:
            tkinter.messagebox.showinfo(title='消息提示', message='今天的抽奖环节到此结束，恭祝大家工作顺利，心想事成！')
            root.quit
        resultList = []
        while root.flag:
            tempint = random.choice(employee)
            if (tempint not in resultList):
                resultList.append(tempint)
            if len(resultList) >= 10:
                arr = np.arange(-len(resultList), 0)
                # print(resultList)
                for i in arr[-1:]:
                    first['text'] = resultList[i]
                    second['text'] = resultList[i - 1]
                    third['text'] = resultList[i - 2]
                    fourth['text'] = resultList[i - 3]
                    fifth['text'] = resultList[i - 4]
                    sixth['text'] = resultList[i - 5]
                    seventh['text'] = resultList[i - 6]
                    eighth['text'] = resultList[i - 7]
                    ninth['text'] = resultList[i - 8]
                    tenth['text'] = resultList[i - 9]
                    time.sleep(0.01)
                resultList = []
            else:
                if len(resultList) == 9:
                    first['text'] = resultList[0]
                    second['text'] = resultList[1]
                    third['text'] = resultList[2]
                    fourth['text'] = resultList[3]
                    fifth['text'] = resultList[4]
                    sixth['text'] = resultList[5]
                    seventh['text'] = resultList[6]
                    eighth['text'] = resultList[7]
                    ninth['text'] = resultList[8]
                if len(resultList) == 8:
                    first['text'] = resultList[0]
                    second['text'] = resultList[1]
                    third['text'] = resultList[2]
                    fourth['text'] = resultList[3]
                    fifth['text'] = resultList[4]
                    sixth['text'] = resultList[5]
                    seventh['text'] = resultList[6]
                    eighth['text'] = resultList[7]
                if len(resultList) == 7:
                    first['text'] = resultList[0]
                    second['text'] = resultList[1]
                    third['text'] = resultList[2]
                    fourth['text'] = resultList[3]
                    fifth['text'] = resultList[4]
                    sixth['text'] = resultList[5]
                    seventh['text'] = resultList[6]
                if len(resultList) == 6:
                    first['text'] = resultList[0]
                    second['text'] = resultList[1]
                    third['text'] = resultList[2]
                    fourth['text'] = resultList[3]
                    fifth['text'] = resultList[4]
                    sixth['text'] = resultList[5]
                if len(resultList) == 5:
                    first['text'] = resultList[0]
                    second['text'] = resultList[1]
                    third['text'] = resultList[2]
                    fourth['text'] = resultList[3]
                    fifth['text'] = resultList[4]
                if len(resultList) == 4:
                    first['text'] = resultList[0]
                    second['text'] = resultList[1]
                    third['text'] = resultList[2]
                    fourth['text'] = resultList[3]
                if len(resultList) == 3:
                    first['text'] = resultList[0]
                    second['text'] = resultList[1]
                    third['text'] = resultList[2]
                if len(resultList) == 2:
                    first['text'] = resultList[0]
                    second['text'] = resultList[1]
                if len(resultList) == 1:
                    first['text'] = resultList[0]
                if len(resultList) == 0:
                    tkinter.messagebox.showinfo(title='消息提示', message='今天的抽奖环节到此结束，恭祝大家工作顺利，心想事成！')

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()
            self.switch()

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()


t = myThread()


def clean_text():
    first['text'] = ''
    second['text'] = ''
    third['text'] = ''
    fourth['text'] = ''
    fifth['text'] = ''
    sixth['text'] = ''
    seventh['text'] = ''
    eighth['text'] = ''
    ninth['text'] = ''
    tenth['text'] = ''


def butStartClick1():
    # 背景音乐
    pygame.init()
    music = pygame.mixer.music.load(r'Bandari - 早晨的空气.mp3')
    pygame.mixer.music.play(-1, 100)
    if t.is_alive():
        t.resume()
        print('已经启动')
    else:
        t.start()
        print('第一次启动线程')
    t.award_level = 1
    # 开始抽奖时先清空label
    clean_text()
    butStop.configure(state='normal')
    btnlevel1.configure(state='disabled')
    btnlevel2.configure(state='disabled')
    btnlevel3.configure(state='disabled')
    btnlevel4.configure(state='disabled')
    btnlevel5.configure(state='disabled')
    btnlevel6.configure(state='disabled')
    # read_two.configure(state='disabled')  # 重新保存读数


btnlevel1 = tkinter.Button(root, text='一等奖', border='5', fg='white', bg='tomato',
                           font=('微软雅黑', 20, 'bold', 'normal'), command=butStartClick1)
btnlevel1.place(x=95, y=150, width=170, height=40)


def butStartClick2():
    if t.is_alive():
        t.resume()
        print('已经启动')
    else:
        t.start()
        print('第一次启动线程')
    t.award_level = 2
    # 开始抽奖时先清空label
    clean_text()
    butStop.configure(state='normal')
    btnlevel1.configure(state='disabled')
    btnlevel2.configure(state='disabled')
    btnlevel3.configure(state='disabled')
    btnlevel4.configure(state='disabled')
    btnlevel5.configure(state='disabled')
    btnlevel6.configure(state='disabled')
    # read_two.configure(state='disabled')  # 重新保存读数


btnlevel2 = tkinter.Button(root, text='二等奖', border='5', fg='white', bg='tomato',
                           font=('微软雅黑', 20, 'bold', 'normal'), command=butStartClick2)
btnlevel2.place(x=295, y=150, width=170, height=40)


def butStartClick3():
    if t.is_alive():
        t.resume()
        print('已经启动')
    else:
        t.start()
        print('第一次启动线程')
    t.award_level = 3
    # 开始抽奖时先清空label
    clean_text()
    butStop.configure(state='normal')
    btnlevel1.configure(state='disabled')
    btnlevel2.configure(state='disabled')
    btnlevel3.configure(state='disabled')
    btnlevel4.configure(state='disabled')
    btnlevel5.configure(state='disabled')
    btnlevel6.configure(state='disabled')
    # read_two.configure(state='disabled')  # 重新保存读数


btnlevel3 = tkinter.Button(root, text='三等奖', border='5', fg='white', bg='tomato',
                           font=('微软雅黑', 20, 'bold', 'normal'), command=butStartClick3)
btnlevel3.place(x=495, y=150, width=170, height=40)


def butStartClick4():
    if t.is_alive():
        t.resume()
        print('已经启动')
    else:
        t.start()
        print('第一次启动线程')
    t.award_level = 4
    # 开始抽奖时先清空label
    clean_text()
    butStop.configure(state='normal')
    btnlevel1.configure(state='disabled')
    btnlevel2.configure(state='disabled')
    btnlevel3.configure(state='disabled')
    btnlevel4.configure(state='disabled')
    btnlevel5.configure(state='disabled')
    btnlevel6.configure(state='disabled')
    # read_two.configure(state='disabled')  # 重新保存读数


btnlevel4 = tkinter.Button(root, text='四等奖', border='5', fg='white', bg='tomato',
                           font=('微软雅黑', 20, 'bold', 'normal'), command=butStartClick4)
btnlevel4.place(x=695, y=150, width=170, height=40)


def butStartClick5():
    if t.is_alive():
        t.resume()
        print('已经启动')
    else:
        t.start()
        print('第一次启动线程')
    t.award_level = 5
    # 开始抽奖时先清空label
    clean_text()
    butStop.configure(state='normal')
    btnlevel1.configure(state='disabled')
    btnlevel2.configure(state='disabled')
    btnlevel3.configure(state='disabled')
    btnlevel4.configure(state='disabled')
    btnlevel5.configure(state='disabled')
    btnlevel6.configure(state='disabled')
    # read_two.configure(state='disabled')  # 重新保存读数


btnlevel5 = tkinter.Button(root, text='五等奖', border='5', fg='white', bg='tomato',
                           font=('微软雅黑', 20, 'bold', 'normal'), command=butStartClick5)
btnlevel5.place(x=895, y=150, width=170, height=40)


def butStartClick6():
    if t.is_alive():
        t.resume()
        print('已经启动')
    else:
        t.start()
        print('第一次启动线程')
    t.award_level = 6
    # 开始抽奖时先清空label
    clean_text()
    butStop.configure(state='normal')
    btnlevel1.configure(state='disabled')
    btnlevel2.configure(state='disabled')
    btnlevel3.configure(state='disabled')
    btnlevel4.configure(state='disabled')
    btnlevel5.configure(state='disabled')
    btnlevel6.configure(state='disabled')
    # read_two.configure(state='disabled')  # 重新保存读数


btnlevel6 = tkinter.Button(root, text='六等奖', border='5', fg='white', bg='tomato',
                           font=('微软雅黑', 20, 'bold', 'normal'), command=butStartClick6)
btnlevel6.place(x=1095, y=150, width=170, height=40)


def btnStopClick():
    global award_level
    global award_time
    global old_data
    root.flag = False
    t.pause()
    if t.award_level == 1:
        award_name = '一等奖:'
        employee_sql = "update employee set flag='一等奖' where name in (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    if t.award_level == 2:
        award_name = '二等奖:'
        employee_sql = "update employee set flag='二等奖' where name in (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    if t.award_level == 3:
        award_name = '三等奖:'
        employee_sql = "update employee set flag='三等奖' where name in (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    if t.award_level == 4:
        award_name = '四等奖:'
        employee_sql = "update employee set flag='四等奖' where name in (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    if t.award_level == 5:
        award_name = '五等奖:'
        employee_sql = "update employee set flag='五等奖' where name in (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    if t.award_level == 6:
        award_name = '六等奖:'
        employee_sql = "update employee set flag='六等奖' where name in (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    first.flag = 'false'
    i0 = first.cget('text')
    i1 = second.cget('text')
    i2 = third.cget('text')
    i3 = fourth.cget('text')
    i4 = fifth.cget('text')
    i5 = sixth.cget('text')
    i6 = seventh.cget('text')
    i7 = eighth.cget('text')
    i8 = ninth.cget('text')
    i9 = tenth.cget('text')
    update_data = [i0, i1, i2, i3, i4, i5, i6, i7, i8, i9]
    old_data = update_data
    # print(update_data)
    my_conn_update(employee_sql, update_data)
    for item in update_data:
        award_name = award_name + item + '、'
    award_name = award_name[:-1]
    Listbox.insert(tkinter.END, award_name)

    def award_numquery():
        Listbox_num.delete(0, tkinter.END)
        items = ['未中奖', '一等奖', '二等奖', '三等奖', '四等奖', '五等奖', '六等奖']
        for i in items:
            sql = "SELECT count(id) FROM employee WHERE flag='%s' " % i
            res = my_conn_select(sql)
            res = i + ':' + str(res[0][0]) + "人"
            Listbox_num.insert(tkinter.END, res)

    award_numquery()
    butStop.configure(state='disabled')
    btnlevel1.configure(state='normal')
    btnlevel2.configure(state='normal')
    btnlevel3.configure(state='normal')
    btnlevel4.configure(state='normal')
    btnlevel5.configure(state='normal')
    btnlevel6.configure(state='normal')
    # read_two.configure(state='normal')
    # read_two()


butStop = tkinter.Button(root, text='停 止', border='5', fg='white', bg='tomato', font=('微软雅黑', 20, 'normal'),
                         command=btnStopClick)
butStop.place(x=800, y=100, width=170, height=40)


def btnResetClick():
    employee_sql = "update employee set flag='未中奖'"
    data = []
    clean_text()
    my_conn_update(employee_sql, data)
    Listbox.delete(0, tkinter.END)
    Listbox_num.delete(0, tkinter.END)
    btnStart1.configure(state='normal')
    btnStart2.configure(state='disabled')
    btnStart3.configure(state='disabled')
    root.mainloop()


btnReset = tkinter.Button(root, text='重 置', border='5', fg='white', bg='tomato', font=('微软雅黑', 20, 'bold', 'normal'),
                          command=btnResetClick)
btnReset.place(x=1000, y=100, width=170, height=40)

btnStart1.configure(state='normal')  # 第一轮
btnStart2.configure(state='disabled')  # 第二轮
btnStart3.configure(state='disabled')  # 第三轮
butStop.configure(state='disabled')  # 停止
btnReset.configure(state='normal')
btnlevel1.configure(state='disabled')  # 一等奖
btnlevel2.configure(state='disabled')  # 二等奖
btnlevel3.configure(state='disabled')  # 三等奖
btnlevel4.configure(state='disabled')  # 四等奖
btnlevel5.configure(state='disabled')  # 五等奖
btnlevel6.configure(state='disabled')  # 六等奖
# read_two.configure(state='disable')  # 重新保存读数
# print(num)
# 启动主程序
root.mainloop()
