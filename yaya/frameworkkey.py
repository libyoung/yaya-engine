#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170515
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     Flow Object
##############################

__all__ = ["FOR","SWITCH","SWITCH2","SWITCHWrapper","SWITCHWrapper2","WHILE",'NOT']

class FOR(object):
    '''
    Framework FOR Key
    '''
    def __init__(self, times = 1, *args, **kwargs):
        self.times = times
        self.steps = []

    def __getitem__(self, steps):
        if isinstance(steps, tuple):
            self.steps.append(steps)
        else:
            self.steps.append((steps,))
        return FORWrapper(self.times, self.steps)

class FORWrapper(object):
    '''
    Framework FOR Key
    '''
    def __init__(self, times, steps):
        self.times = times
        self.steps = steps

    def steps_gene(self):
        if self.times > 0:
            for i in xrange(self.times):
                yield self.steps

    def FlowAction(self, flow):
        '''
        Operate for circulation with generator
        '''
        result = False
        for item in self.steps_gene():
            result = flow.Run(item)
            if not result:
                break
        return result


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
        self.steps = []

    def steps_gene(self):
        for item in self.steps:
            yield item

    def __getitem__(self, key):
        if isinstance(key, tuple):
            self.steps.append(key)
        else:
            self.steps.append((key,))
        return self

    def FlowAction(self, flow):
        '''
        '''
        result = True
        for item in self.steps_gene():
            if flow.Run(item[0]):
                result = flow.Run(item[1:])
                break
        return result


class SWITCHWrapper2(SWITCHWrapper):
    '''
    '''
    def __init__(self, steps):
        self.steps = list(steps)

    def steps_gene(self):
        '''
        '''
        if self.steps == None:
            yield None
        elif len(self.steps) == 1: 
            yield self.steps[0]
        else:
            for item in self.steps:
                yield item

    def __getitem__(self, key):
        '''
        '''
        if isinstance(key, tuple):
            self.steps.append(key)
        else:
            self.steps.append((key,))

        new_sw = SWITCHWrapper2(self.steps)
        self.steps = []
        return new_sw


SWITCH = SWITCHWrapper

SWITCH2 = SWITCHWrapper2([])


class NOT(object):
    '''
    '''
    def __init__(self, *steps):
        self.steps = steps

    def args_gene(self):
        '''
        '''
        if self.steps == None:
            yield None
        elif len(self.steps) == 1: 
            yield self.steps[0]
        else:
            for item in self.steps:
                yield item

    def FlowAction(self, flow):
        '''
        '''
        for item in self.args_gene(): 
            result = flow.Run(item)
            if not result:
                return True
        return False

if __name__ == "__main__":
    print id(SWITCH2)
    b = SWITCH2["dfdf"]["ddd"]
    print id(b)
    print 'sdfsd'
    print id(SWITCH2)
    c = SWITCH2["123"][123]
    print id(c)

    print "end"