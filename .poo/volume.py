# coding=utf-8

import os

mute = os.popen('pactl get-sink-mute @DEFAULT_SINK@').read()
volume = os.popen('pactl get-sink-volume @DEFAULT_SINK@').read()[28:32]
if mute[6] == "否":
    if volume == ' / -':
        print(' 🔈')
    elif int(volume.replace('%','')) > 66:
        print(' 🔊')
    elif int(volume.replace('%','')) > 33 and int(volume.replace('%','')) <= 66:
        print(' 🔉')
    else:
        print(' 🔈')
else:
    print(' 🔇')
