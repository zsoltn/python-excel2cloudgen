#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from utils.utils_excelcloud import handle_excel  

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        ext =  os.path.splitext(event.src_path)[1][1:] 
        if 'xls' in ext:
            handle_excel( event.src_path )                    
            print "Changed file:" + event.src_path  
    
def startWatcher( folder ):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)            
            lockfilename  = folder + "/excelcloud.lock"
            if os.path.exists(lockfilename):
                os.remove(lockfilename)
                os._exit(0)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


