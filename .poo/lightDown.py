# coding=utf-8

import tkinter as tk
import os,signal

root = tk.Tk()
root.configure(bg='#101616')
root.attributes('-type', 'dock')
root.attributes("-topmost", True)
root.geometry('400x70-10-50')

lig = tk.Label(root, bg='#717171')
ght = tk.Label(root)
light = round(float(os.popen('light').read().replace('\n',''))) - 5
if light < 5:
	light == 0
name = tk.Label(root, text='🌕', bg='#101616', fg='#fff', font=('Segoe UI Emoji',16))
os.system('light -U 5')
value = tk.Label(root, text=light, bg='#101616', fg='#fff')
name.place(x=15,y=20,width=35, height=30)
ligwidth = int(310*light/100)
lig.place(x=55,y=30, width=ligwidth, height=10)
ght.place(x=55+ligwidth,y=30, width=310-ligwidth, height=10)
value.place(x=365,y=20, width=30, height=30)

temp = os.popen("ps ax |grep 'python3 /home/poo/.poo/lightDown.py' |grep -v grep").read()
if len(temp.split('\n')) > 2:
    temp = [x for x in temp.split(' ') if x != ''][0]
    os.kill(int(temp),signal.SIGKILL)

root.after(3000, root.destroy)
root.mainloop()