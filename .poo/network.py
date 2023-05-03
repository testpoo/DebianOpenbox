# coding=utf-8

import os

network = os.popen('hostname -I').read()

if network == '\n':
    print('⚠ Down')
else:
    print('📶 Nokia')
