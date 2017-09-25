#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170518
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     Watcher Object
##############################
import random
import string
import re
import time

def genid(pkg, uiid):
    """Given UI object pkg and ui res id generate complete resID"""
    """拼接包名和resID"""
    return ''.join([pkg, ':id/', uiid])

class Watcher(object):
    '''
    '''
    def __init__(self, dev):
        """Initialize all the watchers."""
        """初始化watchers"""
        self.dev = dev
        self.dev.watchers.remove()
        self.txt_watcher(dev, 'internet not available', 'cancel')
        self.txt_watcher(dev, 'connection status', 'cancel')
        self.txt_watcher(dev, 'by using google play', 'accept')
        self.txt_watcher(dev, 'remind me later', 'remind me later')
        self.txt_watcher(dev, 'use reminders to create', 'no thanks')
        self.txt_watcher(dev, 'this network has no internet access', 'Yes')
        self.txt_watcher(dev, 'A large number of multimedia messages', 'OK')
        self.txt_watcher(dev, 'Tag Log', 'OK')
        self.txt_watcher(dev, 'Storage less than', 'FREE UP SPACE')
        self.txt_watcher(dev, 'Close app', 'Close app')
        self.txt_watcher(dev, 'Wi-Fi networks available', 'REMIND ME LATER')
        allow_id = genid('com.android.packageinstaller', 'permission_allow_button')
        self.rid_watcher(dev, allow_id, allow_id)
        notnow_id = genid('com.android.vending', 'not_now_button')
        self.rid_watcher(dev, notnow_id, notnow_id)
        continue_id = genid('com.android.vending', 'continue_button')
        self.rid_watcher(dev, continue_id, continue_id)
        always_btn_id = genid('android', 'button_always')
        self.rid_watcher(dev, always_btn_id, always_btn_id)
        vid_chk_id = genid('com.tct.camera', 'micro_video_guide_checkbox')
        self.rid_watcher(dev, vid_chk_id, vid_chk_id)
        self.itx_watcher(dev, vid_chk_id, 'got it')



    def txt_watcher(self, dev, txt1, txt2):
        """Generate a watcher that matches text."""
        """生成一个watcher"""
        name = ''.join(random.sample(string.ascii_letters, 12))
        txt1 = '(?i)%s.*' % re.escape(txt1)
        txt2 = '(?i)%s.*' % re.escape(txt2)
        dev.watcher(name).when(textMatches=txt1).click(textMatches=txt2)


    def rid_watcher(self, dev, id1, id2):
        """Generate a watcher that matches ID."""
        """生成一个watcher"""
        name = ''.join(random.sample(string.ascii_letters, 12))
        dev.watcher(name).when(resourceId=id1).click(resourceId=id2)


    def itx_watcher(self, dev, id1, txt1):
        """Generate a watcher to check for ID and then click on UI obj by text."""
        """生成一个watcher"""
        name = ''.join(random.sample(string.ascii_letters, 12))
        txt1 = '(?i)%s.*' % re.escape(txt1)
        dev.watcher(name).when(resourceId=id1).click(textMatches=txt1)

    def run(self):
        self.dev.watchers.reset()
        self.dev.watchers.run()
        flag = False
        while self.dev.watchers.triggered:
            flag = True
            self.dev.watchers.reset()
            self.dev.watchers.run()
        time.sleep(0.5)
        return flag
