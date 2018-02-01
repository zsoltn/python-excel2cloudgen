#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of OTC Tool released under MIT license.
# Copyright (C) 2016 T-systems Kurt Garloff, Zsolt Nagy

import imp
import os
from pprint import pprint
from core.pluginbase import pluginbase
from utils.utils_directory import direxcelcloudtype

PluginFolder = os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))),os.pardir , "providers" )
plugins = {}

def load_from_file(filepath):
    mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
    if mod_name.startswith("__init__"): 
        return 
    if file_ext.lower() == '.py':
        py_mod = imp.load_source(mod_name, filepath)
    elif file_ext.lower() == '.pyc':
        py_mod = imp.load_compiled(mod_name, filepath)        
    else:
        return None
    class_inst = getattr(py_mod, mod_name)()
    return class_inst

def collectplugins():    
    possibledirs = os.listdir(PluginFolder)
    for j in possibledirs:
        possibleplugins = os.listdir(os.path.abspath(os.path.join(PluginFolder, j)))    
        for i in possibleplugins:            
            location = os.path.abspath(os.path.join(PluginFolder,j, i))
            plugin = None            
            if os.path.isdir(location) :
                # here is the dir base plugin definition
                if os.path.exists(location + '/' + i + '.py'):    
                    location =  location + '/' + i + '.py'
                elif os.path.exists(location + '/' + i + '.pyc'):    
                    location =  location + '/' + i + '.pyc'
                else:                    
                    plugin = pluginbase()
                    plugin._excelcloudtype =  direxcelcloudtype(location)                    
            if not plugin: 
                plugin = load_from_file(location)
            
            if plugin:
                pluginame = direxcelcloudtype(location)                                
                plugins[pluginame] = plugin
                    
    return plugins

def getplugin(pluginname):    
    plugin = plugins[pluginname]
    return plugin

def init():    
    for pluginname in plugins:
        plugin = getplugin(pluginname) 
        plugin.init()    


if len(plugins) == 0:
    collectplugins()
    
