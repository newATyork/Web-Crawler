import re
import urllib2
import urlparse
from urllib2 import urlopen,URLError,HTTPError


# Purpose: remove ['main.html','index.html','index.jsp','main.htm','index.htm']

URLEnd = ['main.html','index.html','index.jsp','main.htm','index.htm'] 

def RemoveURLEnd(normalLink):  # normalLink: normalized url link
    for endstr in URLEnd:
        if endstr in normalLink:
            startpos = normalLink.find(endstr)
            beforeStr = normalLink[0:startpos]
            if len(normalLink[startpos:]) > len(endstr):
                if normalLink[startpos+len(endstr)] == '/':
                    afterStr = normalLink[startpos+len(endstr)+1:-1]
                else:
                    afterStr = normalLink[startpos+len(endstr):-1]
                return beforeStr + afterStr
            else:
                return beforeStr 
    return normalLink                                 # return the newLink which has removed URLEnd
    

    

# Purpose: check if the http connection and URL are valid. If not, return False

def CheckLink(currentLink):

    url = urlparse.urlparse(currentLink)

    url = RemoveURLEnd(url)
    
    # print url: ===>  ParseResult(scheme='http', netloc='www.mitbbs.com', path='', params='', query='', fragment='')
    
    if url[0] not in ['http','https']:   # skip other protocols like ftp://
        return False,url
    if 'cgi-bin' in url[2]:    #skip the url which includes 'cgi-bin'
        return False,url
    
    try:
        response = urllib2.urlopen(currentLink)
    except HTTPError,e:
        print 'readURL === HTTPError === The server cannot fulfill the request.'
        print 'readURL === HTTPError === Error code:',e.code
                # Here we can easily skip the Not Found or Password-Protected pages.
        return False,url
    except URLError,e:
        print 'readURL === URLError === Failed to reach a server.'
        print 'readURL === URLError === Reason:',e.reason
                # Here we can easily skip URL error.
        return False,url
    except :    # skip other kinds of errors
        return False,url
    return True,url

