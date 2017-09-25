#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##############################
#   Create Time: 20170427
#   Author:      liuyang
#   Email:       czyang.liu@jrdcom.com
#   Content:     Flow Object
##############################
import argparse
from argparse import ArgumentDefaultsHelpFormatter

class CmdLineParser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Argument Parser for MTBF Handler',
                                              formatter_class=ArgumentDefaultsHelpFormatter)
        self.parser.add_argument('-loop', help='specify the current test loop ')
        self.parser.add_argument('-name', help='specify the current text module name')
        self.parser.add_argument('-mode', help='specify test mode')

    def parse(self, input):
        return self.parser.parse_args(input)