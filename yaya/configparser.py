#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Configuration Module"""
import os
import sys
import codecs
from ConfigParser import SafeConfigParser

class NewSafeConfigParser(SafeConfigParser):
    def optionxform(self, optionstr):
        return optionstr


def Get(filename, section, key, vtype=None):
    """Retrieve values from common.ini."""
    """检查从common.ini获取的值"""
    cfg = SafeConfigParser()
    cfgpath = os.path.join(sys.path[0], 'cfg', filename)
    if not os.path.isfile(cfgpath):
        raise IOError('%s NOT FOUND.' % cfgpath)
    with codecs.open(cfgpath, 'r', encoding='utf-8') as f:
        cfg.readfp(f)
    if vtype is None:
        return cfg.get(section, key)
    elif vtype == 'bool':
        return cfg.getboolean(section, key)
    elif vtype == 'float':
        return cfg.getfloat(section, key)
    elif vtype == 'int':
        return cfg.getint(section, key)

def gettimes(section, key, vtype='int'):
    """Retrieve values from common.ini."""
    """检查从common.ini获取的值"""
    cfg = SafeConfigParser()
    mode = Get('common.ini','Default', 'test_type')
    cfgpath = os.path.join(sys.path[0], 'cfg', mode + '_3GLTE.ini')
    if not os.path.isfile(cfgpath):
        raise IOError('%s NOT FOUND.' % cfgpath)
    with codecs.open(cfgpath, 'r', encoding='utf-8') as f:
        cfg.readfp(f)
    if vtype is None:
        return cfg.get(section, key)
    elif vtype == 'bool':
        return cfg.getboolean(section, key)
    elif vtype == 'float':
        return cfg.getfloat(section, key)
    elif vtype == 'int':
        return cfg.getint(section, key)


def sread():
    """Read the stability config file."""
    """读取配置文件"""
    ttype = Get('common.ini','Default', 'test_type')
    ntype = Get('common.ini','Default', 'network_type')
    scfg = NewSafeConfigParser()
    scfgfile = '%s_%s.ini' % (ttype, ntype)
    scfgpath = os.path.join(sys.path[0], 'cfg', scfgfile)
    if not os.path.isfile(scfgpath):
        raise IOError('%s NOT FOUND.' % scfgpath)
    scfg.read(scfgpath)
    return scfg

def Stci(section):
    """Get the total iterations for a test case."""
    """获取case的迭代次数"""
    scfg = sread()
    return sum([int(x[1]) for x in scfg.items(section)])


def get_app_pkg(app_name):
    """Return package name for app name."""
    """获取app的包名"""
    acfg = NewSafeConfigParser()
    acfgpath = os.path.join(sys.path[0], 'cfg','apps.ini')
    if not os.path.isfile(acfgpath):
        raise IOError('%s NOT FOUND.' % acfgpath)
    with codecs.open(acfgpath, 'r', encoding='utf-8') as f:
        acfg.readfp(f)
    return acfg.get('AppsList', app_name)


def apps_get(section):
    """Get dictionary key-value pairs of app names and package names."""
    """获取apps.ini里的包名和app名称"""
    acfg = NewSafeConfigParser()
    acfgpath = os.path.join(sys.path[0], 'cfg','apps.ini')
    if not os.path.isfile(acfgpath):
        raise IOError('%s NOT FOUND.' % acfgpath)
    with codecs.open(acfgpath, 'r', encoding='utf-8') as f:
        acfg.readfp(f)
    return acfg.items(section)