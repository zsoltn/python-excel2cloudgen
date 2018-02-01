#!/usr/bin/env python

from utils.utils_templates import create_plugin_request
from core.pluginbase import pluginbase 
from utils.utils_directory import direxcelcloudtype
    
class openstackclient(pluginbase):
    
    def excelcloudtype(self):    
        return direxcelcloudtype(__file__)
