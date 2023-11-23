# coding=utf-8

import tkinter as tk
import os

root = tk.Tk()
root.geometry('400x90-10-90')
root.attributes('-type','dock')
root.configure(background='#D5D5D5')
root.focus_force()

volumeValue = os.popen('pactl get-sink-volume @DEFAULT_SINK@').read()[28:32]
if volumeValue == ' / -':
    volumeValue = '0'
else:
    volumeValue = volumeValue.replace('%','')

lightValue = round(float(os.popen('light').read().replace('\n','')))

def updateVolume(self):
    value = volume.get()
    os.system('pactl set-sink-volume @DEFAULT_SINK@ ' + str(value) + '%')
    volumeNum['text'] = value

def updateLight(self):
    value = light.get()
    os.system('light -S ' + str(value))
    lightNum['text'] = value

def updateMute():
    os.system('pactl set-sink-mute @DEFAULT_SINK@ toggle')
    mute = os.popen('pactl get-sink-mute @DEFAULT_SINK@').read()[6]
    if mute == '否':
        volumeName['text'] = '📣'
    else:
        volumeName['text'] = '🔇'

def lossfocus(event=None):
    if event.widget == root:
        root.destroy()

volumeName = tk.Button(root, text="📣", bg='#D5D5D5', relief='flat',font=('Segoe UI Emoji',16), command=updateMute)
mute = os.popen('pactl get-sink-mute @DEFAULT_SINK@').read()[6]
if mute == '否':
    volumeName['text'] = '📣'
else:
    volumeName['text'] = '🔇'
volume = tk.Scale(root, from_=0, to=100, sliderlength=10, width=20,orient='horizontal',bg='#828282', showvalue=False, command=updateVolume)
volume.set(volumeValue)
volumeNum = tk.Label(root, text=volumeValue, bg='#D5D5D5')
volumeName.place(x=10,y=10,width=30,height=30)
volume.place(x=50,y=18,width=300,height=14)
volumeNum.place(x=360,y=10,width=30,height=30)
lightName = tk.Label(root, text="🌕", font=('Segoe UI Emoji',16),bg='#D5D5D5')
light = tk.Scale(root, from_=0, to=100, sliderlength=10,width=20, orient='horizontal',bg='#828282', showvalue=False, command=updateLight)
light.set(lightValue)
lightNum = tk.Label(root, text=lightValue,bg='#D5D5D5')
lightName.place(x=10,y=50,width=30,height=30)
light.place(x=50,y=58,width=300,height=14)
lightNum.place(x=360,y=50,width=30,height=30)
root.bind('<FocusOut>', lossfocus)
root.mainloop()
