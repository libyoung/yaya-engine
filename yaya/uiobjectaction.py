#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170427
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     Action Object
##############################
from uiautomator import AutomatorDeviceUiObject
import uiautomator
import time

U = uiautomator.U

PRE_CHECK_UIOBJECT_TIME_MSEC = 10000

def IsGone(flow, uiobject, timeout, *arg, **kword):
    flow.log.GetLogger().debug("wait %ss until gone" % timeout)
    if uiobject.wait.gone(timeout=timeout):
        return True
    else:
        flow.log.GetLogger().debug("UIObject %s is exists!!!" % kword['selector_field'])
        return False

def IsExists(flow, uiobject, timeout, *arg, **kword):
    '''
    '''
    flow.log.GetLogger().debug("wait %ss until display" % timeout)
    if uiobject.wait.exists(timeout=timeout):
        return True
    else:
        flow.log.GetLogger().debug("UIObject %s isn't exists!!!" % kword['selector_field'])
        return False

def __CheckExists__(obj):
    '''
    '''
    def __CheckExists_wrapper__(flow, uiobject, *arg, **kword):
        for i in xrange(6):
            flow.dm.GetRunDevice.watchers.reset()
            if uiobject.wait.exists(timeout=PRE_CHECK_UIOBJECT_TIME_MSEC):
                return obj(flow, uiobject, *arg)
            elif flow.dm.GetRunDevice.watchers.triggered:
                flow.dm.GetRunDevice.watchers.reset()
                continue
            else:
                break
        #raise Exception, "UIObject %s isn't exists!!!" % kword['selector_field']
        flow.log.GetLogger().debug("UIObject %s isn't exists!!!" , kword['selector_field'])
        return False
    return __CheckExists_wrapper__


@__CheckExists__
def Input(flow, uiobject, input_text_func, *arg):
    if uiobject != None:
        uiobject.clear_text()
        if callable(input_text_func):
            input_text = input_text_func()
        else:
            input_text = input_text_func
        uiobject.set_text(input_text)
        flow.log.GetLogger().debug("Input: %s " % input_text)
        return True
    else:
        return False
@__CheckExists__
def Click(flow, uiobject, *arg):
    uiobject.click.wait()
    flow.log.GetLogger().debug("CLick")
    return True

@__CheckExists__
def DoubleClick(flow, uiobject, *arg):
    uiobject.click()
    uiobject.click()
    flow.log.GetLogger().debug("CLick")
    return True

@__CheckExists__
def Swipe(flow, uiobject, touiobject, *arg):
    if touiobject=="up":
        uiobject.swipe.up()
    elif touiobject=="left":
        uiobject.swipe.left()
    return True


@__CheckExists__
def Scroll(flow, uiobject, touiobject, *arg):
    if touiobject == "tobegin":
        uiobject.scroll.toBeginning()
    elif touiobject == "toend":
        uiobject.scroll.toEnd()
    elif touiobject == "forward":
        uiobject.scroll.forward()
    elif touiobject == "backward":
        uiobject.scroll.backward()
    elif isinstance(touiobject, dict):
        uiobject.scroll.to(**touiobject)
    flow.log.GetLogger().debug("scroll to %s",touiobject)
    return True

@__CheckExists__
def LongClick(flow, uiobject, *arg):
    uiobject.long_click()
    flow.log.GetLogger().debug("LongClick")
    return True

@__CheckExists__
def Drag(flow, uiobject, point, *arg):
    uiobject.drag.to(*point)
    flow.log.GetLogger().debug("Drag to %s",point)
    return True


@__CheckExists__
def Gesture(uiobject):
    pass


class UIObjectAction(dict):
    '''
    The class is to build parameters for UiObjectAction
    '''
    def __init__(self, **kwargs):
        self.__fields = {
                            IsGone:       0x01,
                            IsExists:     0x02,
                            Click:      0x04,
                            LongClick:  0x08,
                            Input:      0x10,
                            Scroll:       0x20,
                            Swipe:      0x40,
                            Drag:       0x80,
                            Gesture:    0x100,
                            DoubleClick: 0x200,
                        }

        self.__reverse_fields = {
                            0x01: IsGone,
                            0x02: IsExists,
                            0x04: Click,
                            0x08: LongClick,
                            0x10: Input,
                            0x20: Scroll,
                            0x40: Swipe,
                            0x80: Drag,
                            0x100: Gesture,
                            0x200: DoubleClick,
                        }
        self.__mask = "mask"
        super(UIObjectAction, self).__setitem__(self.__mask, 0)
        for k in kwargs:
            self[k] = kwargs[k]

    def __setitem__(self, k, v):
        if k in self.__fields:
            super(UIObjectAction, self).__setitem__(U(k), U(v))
            super(UIObjectAction, self).__setitem__(self.__mask, self[self.__mask] | self.__fields[k])
        else:
            raise ReferenceError("%s is not allowed." % k)

    def __delitem__(self, k):
        if k in self.__fields:
            super(UIObjectAction, self).__delitem__(k)
            super(UIObjectAction, self).__setitem__(self.__mask, self[self.__mask] & ~self.__fields[k])

    def IsHasAction(self):
        return len(self) - 1
        
    def GetAction(self):
        mask = self[self.__mask]
        if mask == 0:
            yield Click
        elif mask in self.__reverse_fields:
            yield self.__reverse_fields[mask]
        else:
            for item in range(mask.bit_length()):
                b = 1 << item
                if mask & b == b:
                    yield self.__reverse_fields[b]


#################################
# Action after UIObject operate 
#################################
def Check(flow, uiobject, item):
    flow.log.GetLogger().debug("Check if it exists")
    return flow.Run(item)


def WaitTime(flow, uiobject, sec):
    flow.log.GetLogger().debug("sleep %ss" % sec)
    time.sleep(sec)
    return True

class UIObjectFinishAction(dict):
    '''
    The class is to build parameters for UiObjectAction
    '''

    def __init__(self, **kwargs):
        self.__fields = {
                            WaitTime: 0x01,
                            Check: 0x02,
                        }

        self.__reverse_fields = {
                            0x01: WaitTime,
                            0x02: Check,
                        }
        self.__mask = "mask"
        super(UIObjectFinishAction, self).__setitem__(self.__mask, 0)
        for k in kwargs:
            self[k] = kwargs[k]

    def __setitem__(self, k, v):
        if k in self.__fields:
            super(UIObjectFinishAction, self).__setitem__(U(k), U(v))
            super(UIObjectFinishAction, self).__setitem__(self.__mask, self[self.__mask] | self.__fields[k])
        else:
            raise ReferenceError("%s is not allowed." % k)

    def __delitem__(self, k):
        if k in self.__fields:
            super(UIObjectFinishAction, self).__delitem__(k)
            super(UIObjectFinishAction, self).__setitem__(self.__mask, self[self.__mask] & ~self.__fields[k])

    def IsHasAction(self):
        return len(self) - 1

    def GetAction(self):
        mask = self[self.__mask]
        for item in range(mask.bit_length()):
            b = 1 << item
            if mask & b == b:
                yield self.__reverse_fields[b]


if __name__ == "__main__":
     a = UIObjectAction()
     a[Click]=1
     b = a.get_action()
     c = b.next()
     print c


