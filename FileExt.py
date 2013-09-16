import urllib2

AllowMIME = ['text/html','text/plain','application/x-perl','application/x-asap']

# Purpose: get the content type in the header, and filter any types which are not in List "AllowMIME"

def contentType(url):
    try:
        page = urllib2.urlopen(url)
        pageHeaders = page.headers
        #print pageHeaders
        contentType = pageHeaders.getheader('content-type')
        return contentType
    except:
        return None

def FilterMIME(url):
    content_Type = contentType(url)
    if content_Type in AllowMIME:
        return True
    else:
        return False
    

