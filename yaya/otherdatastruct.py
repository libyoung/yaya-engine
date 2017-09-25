#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170629
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     GetValue Object
##############################
class GetValue(object):
    '''
    '''
    def __init__(key, value):
        self.dict = {}
        self.dict[key] = value
    
    def __call__(self,key):
        def getvalue_wrapper(flow):
            value = self.dict[key]
            if callable(value):
                 self.dict[key] = value()
                 return self.dict[key]
            return value
        return getvalue_wrapper

    def __setitem__(self, key, value):
        self.dict[key] = value