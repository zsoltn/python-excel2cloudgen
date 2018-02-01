#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of OTC Tool released under MIT license.
# Copyright (C) 2016 T-systems Kurt Garloff, Zsolt Nagy

from abc import abstractmethod, ABCMeta
import os
import pip
import inspect

from utils.utils_templates import create_plugin_request 
from utils.utils_directory import direxcelcloudtype

class pluginbase:
    _excelcloudtype = None
    
    def __init__(self,*args,**kwargs):
        pass
            
    __metaclass__ = ABCMeta

    #@abstractmethod
    def excelcloudtype(self):
        if self._excelcloudtype == None:
            return direxcelcloudtype(__file__)        
        else:
            return self._excelcloudtype
            
    def init(self):        
        pluginfile = inspect.getfile(self.__class__)
         
        req = os.path.join( os.path.dirname( pluginfile ), "requirements.txt" )
        if not os.path.exists( req ):
            return
         
        with open(req) as f:
            for line in f:
                print line 
                # call pip's main function with each requirement
                pip.main(['install','-U', line])
    
    @staticmethod
    def handleclouddef( self,config, outputdir=None ):        
        self.codegen( outputdir, avar=config)
    
    def codegen( self,outputdir, avar=None ):        
        create_plugin_request( self.excelcloudtype(), outputdir, avar)
        print "Code generated for plugin:" + self.excelcloudtype()