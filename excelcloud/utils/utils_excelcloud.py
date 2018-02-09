#!/usr/bin/env python

from utils_excel import get_cloud_excel_resources
from core.pluginmanager import getplugin
from string import lower
import os
from idlelib import configSectionNameDialog


def handleclouddefs( config, outputdir=None  ): 
    outputdirabs = outputdir               
    if outputdir:
        if os.path.isabs(outputdir):  
            outputdirabs = os.path.abspath(outputdir)                
        else:
            outputdirabs = os.path.join(os.getcwd(),outputdir)                           
        
    for cloud,instances in config["excelclouds"].iteritems():
        newconfig = { 
            "project": cloud,
            "cloudconfig" :{},
            "files" : [],
            "networks" :[],
            "secgroups": [],
            "instances":[]
        }
                        
        for instance in instances:
            if config["templates"] is None or len( instance["TEMPLATE"] ) == 0:
                print "Error with cloud definition:" + cloud 
                os._exit(9)
                                 
            template = config["templates"][str(instance["TEMPLATE"])]
            engine = template["ENGINE"]
            cloudtype= template["CLOUD"]
            
            # merge into template values to clouddefinitions 
            instance.update(template)
            newconfig["instances"].append(instance)
                        
            networkname=str(template["NETWORK"])            
            network = config["networks"][networkname]
            newconfig["networks"].append( network )
            
            secgroupname=str(template["SECGROUP"])
            secgroup = config["secgroups"][secgroupname]
            newconfig["secgroups"].append( secgroup )
                   
            if cloud in config["files"]:             
                files = config["files"][cloud]             
                newconfig["files"].append( files )
            
            cloudconfig = config["cloudconfig"][template["CLOUD"]]
            newconfig["cloudconfig"] = cloudconfig            
                                 
        
        pluginname = lower( cloudtype + "/" + engine  )
        
        getplugin(pluginname).handleclouddef( getplugin(pluginname),newconfig, outputdir=outputdirabs)

"""        
def handleclouddefs_backup( config, outputdir=None  ):
    outputdirabs = outputdir               
    if outputdir:
        if os.path.isabs(outputdir):  
            outputdirabs = os.path.abspath(outputdir)                
        else:
            outputdirabs = os.path.join(os.getcwd(),outputdir)                           
        
    for cloud,vals in config["excelclouds"].iteritems():
        variables = {}
        
        for val in vals:
            if config["templates"] is None or len( val["TEMPLATE"] ) == 0:
                print "Error with:" + cloud 
                continue
                         
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
"""

def handle_excel( excelfile, outputdir=None ):
    config = get_cloud_excel_resources( excelfile )    
    handleclouddefs( config, outputdir=outputdir )
    