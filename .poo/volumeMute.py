# coding=utf-8

import tkinter as tk
import os,signal

root = tk.Tk()
root.configure(bg='#101616')
root.attributes('-type', 'dock')
root.attributes("-topmost", True)
root.geometry('400x70-10-50')

vol = tk.Label(root, bg='#717171')
ume = tk.Label(root)
os.system('pactl set-sink-mute @DEFAULT_SINK@ toggle')
mute = os.popen('pactl get-sink-mute @DEFAULT_SINK@').read()[6]
volume = os.popen('pactl get-sink-volume @DEFAULT_SINK@').read()[28:32]
if volume == ' / -':
	volume = 0
else:
	volume = int(volume.replace('%',''))
if mute == '否':
	volumeText = '🔔'
else:
	volumeText = '🔇'
name = tk.Label(root, text=volumeText, bg='#101616', fg='#fff', font=('',16))
value = tk.Label(root, text=volume, bg='#101616', fg='#fff')
name.place(x=15,y=20,width=35, height=30)
volwidth = int(310*volume/100)
vol.place(x=55,y=30, width=volwidth, height=10)
ume.place(x=55+volwidth,y=30, width=310-volwidth, height=10)
value.place(x=365,y=20, width=30, height=30)

temp = os.popen("ps ax |grep 'python3 /home/poo/.poo/volumeMute.py' |grep -v grep").read()
if len(temp.split('\n')) > 2:
    temp = [x for x in temp.split(' ') if x != ''][0]
    os.kill(int(temp),signal.SIGKILL)

root.after(3000, root.destroy)
root.mainloop()