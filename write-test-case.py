# -*- coding: utf-8 -*-
from yaya import *
'''
验证拨号盘中各按键输入
1.进入电话-->打开拨号盘-->点击键盘上的所有按键进行输入	
1.所有按键均能正常在拨号盘中输入
'''
test_press_all_key = [
    "验证拨号盘中各按键输入",
    "1.进入电话", OpenAPP("Dialer"),
    "2.打开拨号盘", 
    SWITCH()[{'resourceId':'com.android.dialer:id/floating_action_button'}]
           [ Home, OpenAPP("Dialer")],
    "3.点击键盘上的所有按键进行输入",
    {"text":"1"},{"text":"2"},{"text":"3"},
    {"text":"4"},{"text":"5"},{"text":"6"},
    {"text":"7"},{"text":"8"},{"text":"9"},
    {"text":"*"},{"text":"0"},{"text":"#"},
    {"text":"0",LongClick:2},
    #SDevice2[ OpenAPP('Dialer'), Home, Recent],
    #SDevice2[ OpenAPP('Setting'), Home, Recent],
    "验证：所有按键均能正常在拨号盘中输入", CheckExists(textContains="123456789*0#+"),
]

def setup(flow):
    pass

def teardown(flow):
    pass

case_list = [
        ("Press all the key in the Dailer", 20, 1, test_press_all_key, None),
    ]
module_total_time = sum([item[1] for item in case_list])
module_mini_total_time = sum([item[2] for item in case_list])

run_list = StabilityTestTemplate(case_list, setup, teardown)