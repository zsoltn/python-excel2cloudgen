#!/usr/bin/env python

from python_terraform import logging
from python_terraform import Terraform
from python_terraform import IsFlagged
from sys import platform
from sys import stdout

import requests
import os
from utils.utils_directory import extract_zip
from utils.utils_directory import set_executeable 
from utils.utils_templates import create_plugin_request

from utils.utils_templates import create_plugin_request
from core.pluginbase import pluginbase 
from utils.utils_directory import direxcelcloudtype
import tempfile
import shutil


#terraformdir= os.path.join( os.path.dirname(os.path.realpath(__file__)), "terraform")
#terraformdir= os.path.dirname(os.path.realpath(__file__))
terraformdir = os.path.join( tempfile.gettempdir(), "excelcloud-terraform")

terraformtemplatefilename = "provider_template.tf"
terraformtemplatefile = os.path.join( os.path.dirname(os.path.realpath(__file__)), "templates",terraformtemplatefilename)

    
class terraform(pluginbase):    
    def excelcloudtype(self):    
        return direxcelcloudtype(__file__)

    @staticmethod
    def handleclouddef( self,config, outputdir=None  ):
        state = config["#PROJECT NAME"]  + ".state"
        if outputdir is None:
            
            self.codegen(terraformdir, avar=config)                     
            startTerraform(avar=config, astate = state )
        else:            
            outputdir = os.path.abspath(outputdir)                         
            self.codegen( outputdir, avar=config)
                    
                    
    def init(self):            
        # this will be excelcloud --init terraform command
        super(terraform, self).init()
        if not os.path.exists(terraformdir): 
            os.makedirs(terraformdir)         
        download_terraform()        
        startTerraform(init=True)

def download_terraform():            
    if platform == "win32":        
        url = 'https://releases.hashicorp.com/terraform/0.10.7/terraform_0.10.7_windows_amd64.zip'
    elif platform == "linux" or platform == "linux2":
        url = 'https://releases.hashicorp.com/terraform/0.11.0/terraform_0.11.0_linux_amd64.zip'
    elif platform == "darwin":
        url = 'https://releases.hashicorp.com/terraform/0.11.0/terraform_0.11.0_darwin_amd64.zip'
    
    #targetdir  = "terraform"
    targetfile = "terraform.zip"
    
    print terraformdir + "/" + targetfile
    download_terraform_package(url, terraformdir + "/" + targetfile)
    
    extract_zip(terraformdir + "/" + targetfile, terraformdir + "/" )
    
    if not platform == "win32":
        set_executeable( terraformdir + "/" + os.path.splitext(targetfile)[0] )
    
    shutil.copyfile(terraformtemplatefile, os.path.join( terraformdir ,  terraformtemplatefilename)) 
    
def download_terraform_package(url, targetfile):        
    r = requests.get(url, allow_redirects=True)    
    open(targetfile, 'wb').write(r.content)



def init_tf_logger( ):
    logging.basicConfig(level=logging.DEBUG)
    root_logger = logging.getLogger()
    ch = logging.StreamHandler(stdout)
    root_logger.addHandler(ch)

def startTerraform( aworking_dir=terraformdir , aterraform_bin_path=terraformdir + '/terraform', astate= None, avar={}, init = False ):
    os.environ["TF_LOG "] = "TRACE"
    init_tf_logger()
    tf = Terraform(working_dir=aworking_dir, terraform_bin_path=aterraform_bin_path, state = astate )

    if init: 
        tf.init()
    elif int(avar["SIZE"]) != 0: 
        tf.apply(no_color=IsFlagged, refresh=False, var=avar)
    else:
        tf.destroy(var=avar)