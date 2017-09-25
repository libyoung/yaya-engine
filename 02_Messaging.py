#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Telephony Test Case

Specifications:
    * 13340 AT&T Requirements v5.7 Chapter 40
    * 15595 AT&T Test Plan v3.8 Section 5.1.1
"""

from __future__ import absolute_import, division

import sys
import datetime
import random
import string
from yaya import *

contacts_call = {'descriptionContains':'Call Mobile'}
clear=[ClearBackgroundAPP(),SDevice(ClearBackgroundAPP())]
def get_name():
    '''
    '''
    chars = ''.join(random.sample(string.ascii_letters, 4))
    name = '%s_%s' % ('AT', chars.upper())
    return name

backto_contacts = NOT(FOR(4)({'text':'ALL CONTACTS', IsGone:2}, Back))
def vertto(flow):
    mdevice = flow.dm.GetMDevice.GetDevice
    mdevice(scrollable=True).scroll.to(text="Messaging")


Test_send_message_ways=["Test_send_message_ways",SDevice(Back),MDevice(Back),
                        "1.进入短信--.>新建信息",

                        OpenAPP("Messaging"),{"resourceId":"com.android.mms:id/floating_action_button_container"},

                        "2.从联系人中添加联系人",{"resourceId":"com.android.mms:id/recipients_picker"},{"descriptionContains":"AT_"},{"text":"OK"},

                        "3.发送信息（内容为：7bit/16bit/插入文本)",{"resourceId":"com.android.mms:id/embedded_text_editor",Input:"7bit/16bit"},
                        {"resourceId":"com.android.mms:id/send_button_sms"},Wait(5),"Check",

                        "4.创建另一条信息",Back,Back,{"resourceId":"com.android.mms:id/floating_action_button_container"},

                        "5.手动输入联系人",{"resourceId":"com.android.mms:id/recipients_editor",Input:"18651502758"},

                        "6.发送信息（内容为：7bit/16bit/插入文本",{"resourceId":"com.android.mms:id/embedded_text_editor",Input:"7bit/16bit/"},
                        {"resourceId":"com.android.mms:id/send_button_sms"},Wait(5),"Check",
                        clear]
Test_send_message_differentways=["Test_send_message_differentways",SDevice(Back),MDevice(Back),
                                 "1.通过状态栏消息通知发送短信",MDevice(OpenAPP("Dialer")),SDevice(OpenAPP("Messaging"),{"resourceId":"com.android.mms:id/floating_action_button_container"},
                                 {"resourceId": "com.android.mms:id/recipients_editor",Input: "18651503218"},{"resourceId":"com.android.mms:id/embedded_text_editor",Input:"7bit/16bit/"},
                                 {"resourceId": "com.android.mms:id/send_button_sms"},Home,Wait(5)),OpenNotification,{"text":"Messaging"},
                                 {"resourceId":"com.android.mms:id/embedded_text_editor",Input:"7bit/16bit"},{"resourceId":"com.android.mms:id/send_button_sms"},Wait(5),
                                 "Check",SDevice({"text":"CLOSE"}),

                                 "2.通过通话记录发送短信",Home,OpenAPP("Dialer"),'call number', CallNumber("18651502758"),Wait(4),EndCall,{"descriptionContains":"Call history"},{"textContains":"AT_"},
                                 {"text":"Send a message"}, {"resourceId":"com.android.mms:id/embedded_text_editor",Input:"7bit/16bit"},{"resourceId":"com.android.mms:id/send_button_sms"},Wait(5),
                                 "Check",SDevice({"text":"CLOSE"}),

                                 "3.通过联系人发送短信",Home,OpenAPP("Contacts"),{"textContains":"AT_"},{"resourceId":"com.android.contacts:id/icon_alternate"},{"resourceId":"com.android.mms:id/embedded_text_editor",Input:"7bit/16bit"},
                                 {"resourceId":"com.android.mms:id/send_button_sms"},Wait(5),"Check",SDevice({"text":"CLOSE"}),

                                 "4.通过短信小部件/直接小部件发送短信",Home,LongClickXY(186,1033),{"text":"WIDGETS"},vertto,{"text":"3 × 3",Drag:(167,281)},
                                 {"resourceId":"com.android.mms:id/widget_compose"},{"resourceId": "com.android.mms:id/recipients_editor",Input: "18651502758"},{"resourceId":"com.android.mms:id/embedded_text_editor",Input:"7bit/16bit/"},
                                 {"resourceId": "com.android.mms:id/send_button_sms"},Wait(5),"Check",SDevice({"text":"CLOSE"}),

                                 "5.通过短信应用直接发送短信",{"resourceId":"com.android.mms:id/embedded_text_editor",Input:"7bit/16bit/"},
                                 {"resourceId": "com.android.mms:id/send_button_sms"},Wait(5),"Check",SDevice({"text":"CLOSE"}),

                                 "6.通过“消息弹出框”发送短信",Home,{"textContains":"AT_",Drag:(384,41)},SDevice(OpenAPP("Messaging"),{"resourceId":"com.android.mms:id/floating_action_button_container"},
                                 {"resourceId": "com.android.mms:id/recipients_editor",Input: "18651503218"},{"resourceId":"com.android.mms:id/embedded_text_editor",Input:"7bit/16bit/"},
                                 {"resourceId": "com.android.mms:id/send_button_sms"},Home,Wait(5)),{"text":"VIEW"},{"resourceId":"com.android.mms:id/embedded_text_editor",Input:"7bit/16bit/"},
                                 {"resourceId": "com.android.mms:id/send_button_sms"}, Wait(5), "Check", SDevice({"text": "CLOSE"}),
                                 clear
                                ]

Test_get_message_include_differenttype=["Test_get_message_include_differenttype",SDevice(Back),MDevice(Back),
                                        SDevice(OpenAPP("Messaging"),{"resourceId":"com.android.mms:id/floating_action_button_container"},
                                        {"resourceId": "com.android.mms:id/recipients_editor",Input: "18651503218"},{"resourceId":"com.android.mms:id/embedded_text_editor",Input:"7bit/167bit/16bit/*****%%%%$$$##@@@!7bit/167bit/16bit/*****%%%%$$$##@@@!()()()^$@@$%$bit()()()^$@@$%$bit/*****7b7bit/16bit/*****%%%%$$$##@@@!()()()^$@@$%$it/16bit/*****%%%%$$$##@@@!()()()^$@@$%$%%%%$$$##@@@!()()()^$@@$%$"},
                                        {"resourceId": "com.android.mms:id/send_button_sms"},Home,Wait(5)),"Check",MDevice({"text":"CLOSE"})
                                        ]

Test_reply_message_from_talk=["Test_reply_message_from_talk",SDevice(Back),MDevice(Back),

                              ]
ll=[ "Step8 call from recent",OpenAPP('Dialer'),Home,SelectBackgroundAPP("Phone")]

Test_Call_from_search=["Test_Call_from_search","Open dialer",OpenAPP("Dialer"),
                       "Serarch 1",{'resourceId':"com.android.dialer:id/search_view_container",Input:1},
                       "Click the serach",SWITCH()[{"textContains":"1"}],
                       "Mdevice is incall",IsInCall(5),
                       "Stay call connect 5s", InCallStay(5),
                       'MDevice end call', EndCall,clear
                        ]
def setup(flow):
    pass

def teardown(flow):
    pass

#######################
# 
#######################
case_list = [
        #('Contacts3G', 20, 2, test_call_from_contacts_3G, MDevice(EndCall, backto_contacts)),
        #('Contacts3GLTE', 60, 2, test_call_from_contacts_LTE, MDevice(EndCall, backto_contacts)),
        #('History3G', 20, 5, Test_Call_from_search, MDevice(EndCall, backto_contacts)), 
        #('History3GLTE',60, 2, test_call_from_history_LTE , MDevice(EndCall, backto_contacts)),
        #('CallReceive', 100, 2,test_call_receive, SDevice(EndCall, backto_contacts)),
        #('ContactsAdd', 20, 2, test_contacts_add, MDevice(EndCall, backto_contacts)),
        #('ContactsDel', 20, 2, test_contacts_remove, MDevice(EndCall, backto_contacts)),
        ("Send message ways",20,1,Test_send_message_ways,clear),
        #("Send message from different ways",20,1,Test_send_message_differentways,clear),
    #("Get differt type message",20,1,Test_get_message_include_differenttype,clear),
    #("Reply message from talk",20,1,ll,clear),
        ]

module_total_time = sum([item[1] for item in case_list])
module_mini_total_time = sum([item[2] for item in case_list])

run_list = StabilityTestTemplate(case_list, setup, teardown)

if __name__ == '__main__':
    import run
    run.main(modu='Messaging')
