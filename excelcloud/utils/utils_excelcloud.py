#!/usr/bin/env python

from utils_excel import get_cloud_excel_resources
from core.pluginmanager import getplugin
from string import lower
import os

def handleclouddefs( config, outputdir=None  ):    
    #variables = generate_variables(config)    
    for cloud,vals in config["excelclouds"].iteritems():
        #from pprint import pprint ; pprint( vals)
        variables = {}
        if config["templates"] is None or len( vals["TEMPLATE"] ) == 0:
            print "Error with:" + cloud 
            continue
        template = config["templates"][str(vals["TEMPLATE"])]

        networkname=str(template["NETWORK"])
        network = config["networks"][networkname]

        secgroupname=str(template["SECGROUP"])
        secgroup = config["secgroups"][secgroupname]
                
        files = None
        if cloud in config["files"]:             
            files = config["files"][cloud] 
        cloudconfig = config["cloudconfig"][template["CLOUD"]]
        variables = generate_key_values ( cloud, vals, cloudconfig , template, files, network,secgroup )
        
        pluginname = lower( variables["CLOUD"] ) + "/"+ lower(variables["ENGINE"] )
        
        outputdirabs = outputdir
               
        if outputdir:
            if os.path.isabs(outputdir):  
                outputdirabs = os.path.abspath(outputdir)                
            else:
                outputdirabs = os.path.join(os.getcwd(),outputdir)                           
                
        getplugin(pluginname).handleclouddef( getplugin(pluginname),variables, outputdir=outputdirabs)
        
    
def generate_key_values( cloud, vals, cloudconfig, template, files,networks,secgroup ):     
    variables = { }
    for cc in cloudconfig:
        variables[cc] = cloudconfig[cc]
    for t in template:
        variables[t] = template[t]
    for v in vals:
        variables[v] = vals[v]
    for v in networks:
        variables[v] = networks[v]
    for v in secgroup:
        variables[v] = secgroup[v]
    
    variables["jumphost_count"] = variables["SIZE"] 
    variables["project"] = cloud

    return variables

def handle_excel( excelfile, outputdir=None ):
    config = get_cloud_excel_resources( excelfile )    
    handleclouddefs( config, outputdir=outputdir )
    