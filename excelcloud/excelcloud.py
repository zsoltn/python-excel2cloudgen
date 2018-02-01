#!/usr/bin/python

import os
from argparse import ArgumentParser, RawTextHelpFormatter
from threading import Thread
from core import pluginmanager
from core.server_sample import startwebdav
from core.exfilesystemwatcher import startWatcher
from utils.utils_excelcloud import handle_excel

def main(argv = None): # IGNORE:C0111
    rootpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "excels")
    parser = ArgumentParser(prog = "excelcloud", formatter_class = RawTextHelpFormatter)
    
    parser.add_argument("--execute",
                        dest = "FILE",
                        help = "Excel file to process.")
    parser.add_argument("--gencode",
                        dest = "CODEPATH",
                        help = "Output directory for generated code.")
    parser.add_argument("--initplugins",
                        dest = "INITPLUGIN",
                        help = "Initialize plugins (if needed).",
                        action = "store_true")
    parser.add_argument("--startserver",
                        dest = "START_SERVER",
                        help = "Start ExcelCloud server application.",
                        action = "store_true")
    parser.add_argument("--stopserver",
                        dest = "STOP_SERVER",
                        help = "Stop ExcelCloud server application.",
                        action = "store_true")
    parser.add_argument("--path",
                        dest = "PATH",
                        help = "Root path of ExcelCloud server.")
    
    # still have to implement the authentication method for Webdav:
    # parser.add_argument("--password",
    #                     dest = "PASSWORD",
    #                     help = "Password of Webdav ExcelCloud server.")
    
    args = parser.parse_args()
    
    if args.PATH:
        rootpath = args.PATH

    if args.CODEPATH and args.FILE:
        # just generate code, but do not execute it
        handle_excel(args.FILE,outputdir = args.CODEPATH)
    elif args.FILE:
        handle_excel(args.FILE)
    elif args.START_SERVER:
        print("Starting file system change watcher.")
        t = Thread(target = startWatcher, args = (rootpath,))
        t.start()
        
        print("Starting Webdav server.")
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
