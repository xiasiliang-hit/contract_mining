# this file is the enter point of the multi-threads content crawling
import Queue;
import threading;
import time;
import pdb;
import sys;

import crawl;
import io;

nThread = 64;

class ThreadUrl(threading.Thread):    
    def __init__(self, queue):
        threading.Thread.__init__(self);
        self.queue = queue;
          
    def run(self):
        while True:
            
            if self.queue.empty():
                break;
            else:
            #running job of one thread, multi-obj will be in parallel
                themeLinkTuple = self.queue.get();
            
                typeName = themeLinkTuple[0];
                themeList = themeLinkTuple[1];
                linkList = themeLinkTuple[2];
                crawl.crawlContent(typeName, themeList, linkList);
            
            #signals to queue job is done
                self.queue.task_done();
                print ("global contentCount: " + str(crawl.contentCount));
                
def crawlContentMultiThread(typeDict):
    queue = Queue.Queue();
           
    #populate queue with data   
    for key, di in typeDict.iteritems():
        themeList = di.keys();
        linkList = di.values();
        tp = (key, themeList, linkList);
        queue.put(tp);
        
    #spawn a pool of threads, and pass them queue instance 
    for i in range(nThread):
        t = ThreadUrl(queue);
        t.setDaemon(True);
        t.start()
                   
    #wait on the queue until everything has been processed     
    queue.join()
    return;

def main():
#    pdb.set_trace();
    sys.stdout = open(io.dataDir + io.logFile, "w");
    start = time.time();
    io.mkdirDataRepo();
    #read from existing type index
    typeDict = io.readType(io.readIndex());      
    crawlContentMultiThread(typeDict);
    print("nThread: " + str(nThread));
    print("Time used: %s" % (time.time() - start));

    return;

def test():
    for i in range(10):
        crawl.test();
    print crawl.contentCount;

if __name__ == "__main__":
    main();
