#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170515
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     Flow Object
##############################

__all__ = ["FOR","SWITCH","SWITCHWrapper","WHILE",'NOT']

class FOR(object):
    '''
    Framework FOR Key
    '''
    def __init__(self, times = 1, *args, **kwargs):
        self.times = times
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        def FORGenerator(flow):
            if self.times > 0:
                for i in xrange(self.times):
                    yield args
        return FORGenerator


class WHILE(object):
    '''
    Framework WHILE Key
    '''
    def __init__(self, uiobject = None, existsorgone = True, *args, **kwargs):
        self.existsorgone = existsorgone
        self.uiobject = uiobject
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        '''

        '''
        def WHILEGenerator(flow):
            '''

            '''
            if self.uiobject != None:
                if existsorgone:
                    checkpoint = flow.rundevice(**self.uiobject).wait.exists
                else:
                    checkpoint = flow.rundevice(**self.uiobject).wait.gone
                while checkpoint():
                    yield args
        return WHILEGenerator


class SWITCHWrapper(object):
    '''
    Framework SWITCH Key
    '''
    def __init__(self):
        self.args = []

    def __call__(self, flow):
        if self.args == None:
            yield None
        elif len(self.args) == 1: 
            yield self.args[0]
        else:
            for item in self.args:
                yield item

    def __getitem__(self,key):
        if isinstance(key, tuple):
            self.args.append(key)
        else:
            self.args.append((key,))
        return self

SWITCH = SWITCHWrapper



class NOT(object):
    '''
    '''
    def __init__(self, *arg):
        self.args = arg


if __name__ == "__main__":
    b = SWITCH("dfdf")
    print b("dd")