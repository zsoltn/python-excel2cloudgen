#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of OTC Tool released under MIT license.
# Copyright (C) 2016 T-systems Kurt Garloff, Zsolt Nagy

import os
from jinja2 import Environment, FileSystemLoader

def render_template(template_filename, context):
    templateFolder = os.path.dirname(os.path.realpath(template_filename))

    TEMPLATE_ENVIRONMENT = Environment(
        autoescape=False,
        loader=FileSystemLoader(templateFolder), #
        trim_blocks=False)
    
    return TEMPLATE_ENVIRONMENT.get_template(os.path.basename(template_filename)).render(context)

def create_plugin_request(pluginname,outputdir, templateConfig ):            
    templateFolder = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),os.pardir, "providers", pluginname,"templates"))    
    possibletemplates = os.listdir(os.path.abspath(templateFolder))
      
    for i in possibletemplates:
        template_file_name = os.path.abspath(os.path.join(templateFolder,i))   
        if os.path.isdir(template_file_name):
            continue     
        
        
#        print outputdir 
#        print templateConfig["project"]
                
        
        outdirwithproject = os.path.join(outputdir,templateConfig["project"])        
        if not os.path.exists(outdirwithproject):
            os.makedirs(outdirwithproject)
        outputfile= os.path.abspath(os.path.join(outdirwithproject, i))
        with open(outputfile, 'w') as f:
            req = render_template(template_file_name, templateConfig )            
            f.write(req)
    return req
    