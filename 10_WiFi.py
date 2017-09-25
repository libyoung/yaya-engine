
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division

import sys
import datetime
import random
import string
from yaya import *

contacts_call = {'descriptionContains':'Call Mobile'}

def get_name():
    '''
    '''
    chars = ''.join(random.sample(string.ascii_letters, 4))
    name = '%s_%s' % ('AT', chars.upper())
    return name
def vertto(flow):
    mdevice = flow.dm.GetMDevice.GetDevice
    mdevice().scroll.to(text="Apps")



test_wifi_on_off=[SDevice("Test wifi on and off",'Launch setiings',
                  OpenAPP("Setting"),Wait(1),SWITCH()[{"resourceId": 'com.android.settings:id/dashboard_tile',"index":5}],
                  'wifi turn ON',SWITCH()[{'text':'Off'}],
                  'wifi turn OFF',SWITCH()[{'text':'On'}])]
test_wifi_connect=[ "Test wifi connect","Launch settings",
                    OpenAPP("Setting"),{"resourceId": 'com.android.settings:id/dashboard_tile',"index":5},
                    'wifi connect',SWITCH()[{"text":'Connected'}]
                    [{"text":"Authentication problem"},{'text':"FORGET"}]
                    [{"text":"Saved"},{'text':"CONNECT"}]
                    [{"text":'AntiGFW_Tools_Only'},{'resourceId':"com.android.settings:id/password",Input:'4esz5RDX',WaitTime:3},{'text':"CONNECT",WaitTime:3}],
                    'wifi forget',SWITCH()[{"text":'Connected'},{'text':"FORGET"}]]
test=["Test APP connect","Launch settings",OpenAPP("Setting"), vertto,
                   {"text": 'Apps',WaitTime:3},Back]
def setup(flow):
    pass

def teardown(flow):
    pass

#######################
#
#######################
case_list = [
        #('WiFi ON/OFF', 20, 2, test_wifi_on_off,None),
        #("WiFi Connect",20, 2,test_wifi_connect,None),
        ("APPS",20,2,test,None)
        ]

module_total_time = sum([item[1] for item in case_list])
module_mini_total_time = sum([item[2] for item in case_list])

run_list = StabilityTestTemplate(case_list, setup, teardown)

if __name__ == '__main__':
    import run
    run.main(modu='WiFi')