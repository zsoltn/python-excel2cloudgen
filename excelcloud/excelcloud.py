#!/usr/bin/python

from threading import Thread
from core.server_sample import startwebdav
import os
from argparse import ArgumentParser, RawTextHelpFormatter
from core import pluginmanager
from core.exfilesystemwatcher import startWatcher
from utils.utils_excelcloud import handle_excel

def main(argv = None): # IGNORE:C0111
    rootpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "excels")
    parser = ArgumentParser(prog = "excelcloud" , formatter_class = RawTextHelpFormatter)
    
    parser.add_argument("--execute", dest = "FILE", help = "Excel file what will processed")
    parser.add_argument("--gencode", dest = "CODEPATH", help = "Path of generated code")
    parser.add_argument("--initplugins", dest = "INITPLUGIN", help = "initializing the plugins (if need)", action = "store_true")
    parser.add_argument("--startserver", dest = "START_SERVER", help = "Start ExcelCloud Server application",action = "store_true")
    parser.add_argument("--stopserver", dest = "STOP_SERVER", help = "Stop ExcelCloud Server application",action = "store_true")
    parser.add_argument("--path", dest = "PATH", help = "Root Path of ExcelCloud Server")
    
    # have to implement the authentication method for WEBDAV
    #parser.add_argument("--password", dest = "PASSWORD", help = "Password of WEBDAV ExcelCloud Server")
    
    args = parser.parse_args()
    
    if args.PATH:
        rootpath = args.PATH

    if args.CODEPATH and args.FILE:
        # not execute the code just generate
        handle_excel(args.FILE,outputdir = args.CODEPATH)
    elif args.FILE:
        handle_excel(args.FILE)
    elif args.START_SERVER:
        print "Start File System Changes Wathcer"
        t = Thread(target = startWatcher, args = (rootpath,))
        t.start()
        
        print "Start WEBDAV server"
        t2 = Thread(target = startwebdav, args = (rootpath,))
        t2.start()
    elif args.INITPLUGIN:
        pluginmanager.init()
    elif args.STOP_SERVER:
        lockfilename = rootpath + "/excelcloud.lock"
        if os.path.exists(lockfilename):
            os.unlink(lockfilename)
        else:
            fp = open(lockfilename, "w")
            fp.flush()
    else:  
        parser.print_help()
        os._exit(0)

if __name__ == "__main__":
    main()
