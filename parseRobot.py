import robotparser
import urllib

# According to "Library for robots.txt parsing in Python" "http://docs.python.org/2/library/robotparser.html",
# here I define Function "findBase" to concatenate "protocol/scheme" and "host/netloc", and return it; and Function "accessRight" to judge
# if this page can be allowed to access.


def findBase(url):
    proto, rest = urllib.splittype(url)   #get protocol/scheme  and  rest of this url
    if proto is None:
       raise ValueError, "unknown URL type: %s" % url

    host, rest = urllib.splithost(rest)  # get host/netloc
    return 'http://' + host


def accessRight(currentURL):
    try:
        rp = robotparser.RobotFileParser()
        robotpath = findBase(currentURL) + '/robots.txt'
        print 'Robotpath is : ', robotpath
        rp.set_url(robotpath)
        rp.read()
        print 'Robots.txt === HTTP Status Code is: ', rp.errcode
        temp = rp.can_fetch("*", currentURL)
        print 'Acess right of my Robot is : ', temp
        return temp
    except:
        print 'Acess right of my Robot is : False'                 
        return False


