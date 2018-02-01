#!/usr/bin/env python

from datetime import datetime
import os
import stat
import zipfile

def direxcelcloudtype(f):        
    i = -1
    if os.path.isfile(f):
        i -= 1   
    provider = f.replace("\\","/").split('/')[i]
    engine = f.replace("\\","/").split('/')[i-1]                    
    return engine+"/" + provider 



def set_executeable( filename ):
    st = os.stat(filename )
    os.chmod(filename , st.st_mode | stat.S_IEXEC)


def extract_zip( zfile, directory_to_extract_to):    
    zip_ref = zipfile.ZipFile(zfile, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()

def read_templatefilenames( excelcloudfolder ):    
    projectres = { }
    for subdir, dirs, files in walklevel ( excelcloudfolder ):
        projectfiles = []
        projectdirs = []

        for dir in dirs:
            for subdir2, dirs2, files2 in walklevel ( os.path.join(subdir, dir),level=-1 ): 
                for projfile in files2:
                    projectfiles.append(os.path.join(subdir2, projfile))
                for projdir in dirs2:
                    projectdirs.append(os.path.join(subdir2, projdir))
            projectres[dir] = { "dirs": projectdirs ,"files": projectfiles }            

    return projectres



def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this and  level != -1:
            del dirs[:]
        yield root, dirs, files

