# coding=utf-8

import os

mute = os.popen('pactl get-sink-mute @DEFAULT_SINK@').read()
volume = os.popen('pactl get-sink-volume @DEFAULT_SINK@').read()
if mute[6] == "否":
    print(' | ♪ '+volume[29:32])
else:
    print(' | ∅ '+volume[29:32])
