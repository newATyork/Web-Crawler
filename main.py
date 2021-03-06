import qQueue
import time
import parseRobot
import re
import urlparse
import LinksExtract
import HTMLParser
import urllib, htmllib, formatter
from initialURLs import *
from normalizeLink import *
from FileExt import *


save = r'd:\webcrawl\data3\poly'   #  the path to store crawled files


def savePage(url,save,pageID):    #  save the crawled files
    timestamp = time.time()
        
    save2 = save + str(pageID)   

    page = urllib.urlretrieve(url,save2)


def WebCrawl( initial_urls , max_depth , max_pages ):   # get Top N results from google, set max depth and max pages you need 

    TocrawlQueue  = qQueue.qQueue()                     # BFS uses a queue here

    for item in initial_urls:
        TocrawlQueue.enqueue(item)

    starttime = time.time()

    Crawled = []                            # make a List which can store info about visited urls in visiting order.  
    CrawledSuccessful = {}                  # make a Dict which can store Key(url) and Value(depth,timestamp,size,feedback);
                                                 # also remove duplicates.
    Next_layer_Set = set([])                # make a Set which can store URLs gotten from pages of URLs in the queue. (next depth)
    depth = 0
    PageID = 1

    while ( TocrawlQueue.size()> 0 or len(Next_layer_Set)> 0) and depth <= max_depth and len(CrawledSuccessful) < max_pages : # if Depth or numOfPages reaches a threshold, while-loop
                                                                                # will stop   
        currentURL = TocrawlQueue.dequeue()


        print '========================================================='
        print 'PageID : ',PageID
        print 'Current URL is: ',currentURL
        print 'Depth is: ',depth
        print 

        tempList = [currentURL,depth]
                
        if currentURL not in CrawledSuccessful.keys() :  # judge if current URL belongs to Dict CrawledSuccessful's keys

            Status,URL = CheckLink(currentURL)
            if Status == False or parseRobot.accessRight(currentURL) == False or FilterMIME(currentURL)== False:
                                                        # if an invalid or forbidden page or disallowed MIME type , skip it
                tempList.append(time.time())            #timestamp
                tempList.append(0)                      #length
                tempList.append('Failure/filter')       # error/feedback
                Crawled.append(tempList)
                if TocrawlQueue.size() == 0:            # if the queue is empty, put all URLs from Next_layer_Set into it. 
                    for unsign in range(len(Next_layer_Set)):
                        TocrawlQueue.enqueue(Next_layer_Set.pop())
                    depth = depth + 1                   # Next layer begins
                PageID = PageID + 1
                continue        # skip this iteration
            else :
                
                try:
                    format = formatter.NullFormatter()                  # create default formatter
                    htmlparser = LinksExtract.LinksExtractor(format)        # create new parser object

                    data = urllib.urlopen(currentURL)
                    tempvar = data.read()
                    lengthOfPage = len(tempvar)                 # get the file's size
                    htmlparser.feed(tempvar)                    # parse the file saving the info about links
                    htmlparser.close()

                    Links_To_Get = htmlparser.get_links()       # get a list of fetched url links

                    for link in (Links_To_Get.pop(0) for _ in xrange(len(Links_To_Get))):  # normalize the urls (e.g. relative path)
                        if link.startswith('/'):
                            link = 'http://' + URL[1] + link
                        elif link.startswith('#'):
                            link = 'http://' + URL[1] + URL[2] + link
                        elif not link.startswith('http'):
                                link = 'http://' + URL[1] + '/' + link
                        if link not in CrawledSuccessful:
                            Next_layer_Set.add(link)
                            
                    savePage(currentURL,save,PageID) 
                    
                    tempList.append(time.time())         #timestamp
                    tempList.append(lengthOfPage)        #length
                    tempList.append('Successful')        #error/feedback
                    Crawled.append(tempList)

                    CrawledSuccessful[currentURL]= tempList   # create a new (key,value) pair in the dict

                    PageID = PageID + 1


                except:
                    tempList.append(time.time())            #timestamp
                    tempList.append(0)                     #length
                    tempList.append('Failure/filter')       #error/feedback
                    Crawled.append(tempList)
                    if TocrawlQueue.size() == 0:  
                        for unsign in range(len(Next_layer_Set)):
                            TocrawlQueue.enqueue(Next_layer_Set.pop())
                        depth = depth + 1
                    PageID = PageID + 1
                    continue
               
        else :    
            tempList.append(time.time())  #timestamp
            tempList.append(0)  # length: should be 0; however, -1 in past logs can is a flag on duplicates of visited URLs on testing.
            #tempList.append(-1) 

            tempList.append('duplicate')  # error/feedback
            Crawled.append(tempList)

            PageID = PageID + 1
        
        if TocrawlQueue.size() == 0:  
            for unsign in range(len(Next_layer_Set)):
                TocrawlQueue.enqueue(Next_layer_Set.pop())
            depth = depth + 1

    endtime = time.time()

    totaltime = endtime - starttime    

    return Crawled, CrawledSuccessful,totaltime



def showCrawledLog(Crawled):
    print
    print
    print
    print '############################Print  out  the  log  of  crawled  pages:#######################################'
    print 'URL                                                              depth    timestamp     length       feedback'
    for each in Crawled:
        for item in each:
            print item,
            print '     ',
        print 


def showCrawledSuccessfulLog(CrawledSuccessful):
    print
    print
    print
    print '############################Print  out  the  log  of  successfully-crawled  pages:###########################'
    print 'URL                                                               depth    timestamp     length       feedback'
    for item in CrawledSuccessful.values():
        for each in item:
            print each,
            print '    ',
        print
        

def showTotalSize(CrawledSuccessful):
    sum = 0
    for item in CrawledSuccessful.values():
        sum = sum + item[3]
    return sum


#########################################################################################################################    

if __name__ == '__main__':

            
    initial_urls = GoogleSomeURLS('NYU poly',10)  # Top 10 results

    crawled,crawled_successful,total_time = WebCrawl(initial_urls, 10, 1000)  # max_depth is 10; max_pages is 1000

    showCrawledLog(crawled)
    showCrawledSuccessfulLog(crawled_successful)

    print
    print 
    print '##############################################################################################################'
    print 'The total number of successfully-downloaded pages: ', len(crawled_successful)
    print

    print 
    print '##############################################################################################################'
    print 'The total size of successfully-downloaded pages: ',showTotalSize(crawled_successful)

    print 
    print '##############################################################################################################'
    print 'The total download time : ',total_time

        
  
    
