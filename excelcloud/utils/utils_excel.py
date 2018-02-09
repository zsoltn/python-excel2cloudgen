#!/usr/bin/env python
import json
import xlwt
import xlrd
from utils_directory import read_templatefilenames  
import os
from django.template.defaultfilters import pprint

def create_workbook(inventory_dict, output_file='inventory.xls'):            
    wb = xlwt.Workbook()
    sheet = wb.add_sheet("servers")
            
    create_sheet(sheet, inventory_dict)
    wb.save(output_file)


def create_sheet(sheet, itemlist):    
    style0 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on',num_format_str='D-MMM-YY' )
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
    style0.pattern = pattern
    
    if isinstance(itemlist, list):
        rowc = 1
        for item in itemlist:            
            if isinstance(item, dict):
                colc = 0
                for k,v in item.items():
                    # here this is a dict of the keys
                    v2 = v
                    if isinstance(v, dict):                     
                        v2 = json.dumps( v ) 
                    if rowc == 1:
                        sheet.write(rowc-1, colc, k,style0)
                    sheet.write(rowc, colc, str(v2))
                    colc = colc + 1
            else :
                raise  KeyError ("not support embeded list")
            rowc= rowc + 1  
        
        
def create_output(inventory_dict, output_file='inventory.xls'):        
    if not output_file: 
        raise KeyError( "Output File Mandatory!")
    create_workbook( inventory_dict, output_file )
    

    
    
def read_config_sheet( sheet ):
    config = {}
    for i in range(sheet.nrows): 
        cloud = sheet.cell_value(i, 0)
        key = sheet.cell_value(i, 1)
        val = sheet.cell_value(i, 2)
        if  not str(cloud).startswith( '#' ):
            if cloud in config: 
                config[cloud][key] = val
            else:
                config[cloud] = { key:val }            
    return config
"""
def read_excelcloud_sheet( sheet ):     
    config = {}    
    for i in range(sheet.nrows):
        cloud = sheet.cell_value(i, 0)
        if( i < 2 ) or cloud.startswith( '#' ) or len(cloud.strip()) ==  0:
            continue
        for j in range(sheet.ncols):                         
            key = sheet.cell_value(1, j)
            val = sheet.cell_value(i, j)
                                    
            if cloud in config :                                      
                config[cloud][key] =  val
            else:
                config[cloud] = { key:val }
    return config

"""
def read_excelcloud_sheets( sheet, multiple=False ):     
    config = {}    
    for i in range(sheet.nrows):
        cloud = sheet.cell_value(i, 0)
        if( i < 2 ) or cloud.startswith( '#' ) or len(cloud.strip()) ==  0: 
            continue

        tempvalues = {}      
        for j in range(sheet.ncols):                               
            key = sheet.cell_value(1, j)
            val = sheet.cell_value(i, j)            
            tempvalues[key] = val            
        if not cloud in config:
            if multiple:
                config[cloud] = []
            else:    
                config[cloud] = tempvalues            
        if multiple:            
            config[cloud].append( tempvalues )
    return config

    
def get_cloud_excel_resources( excelfile ):
    config = {}
    workbook = xlrd.open_workbook(excelfile)

    configsheet = workbook.sheet_by_name("Config")    
    config["cloudconfig"] = read_config_sheet( configsheet )
    
    ecsheet = workbook.sheet_by_name("ExcelCloud")    
    config["excelclouds"] = read_excelcloud_sheets( ecsheet, multiple=True )
    
    templatesheet = workbook.sheet_by_name("Templates")    
    config["templates"] = read_excelcloud_sheets( templatesheet )

    templatesheet = workbook.sheet_by_name("Networks")    
    config["networks"] = read_excelcloud_sheets( templatesheet )

    templatesheet = workbook.sheet_by_name("SecurityGroups")    
    config["secgroups"] = read_excelcloud_sheets( templatesheet )

    
    # read to dict what key contains the projects (folder name) and subdirectory and files name array the full values     
    config["files"] = read_templatefilenames( os.path.dirname(excelfile) + '/projectfiles' )
    config["excelfile"] = excelfile
    config["rootdir"] = os.path.dirname(excelfile)
    
    return config
