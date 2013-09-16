import json
import urllib 

googleURL = ['http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s',
              'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s&start=%d']

# Purpose: get a certain number of google url results in descending order of importance

def GoogleSomeURLS(keywords,num):    
   
    out = []
    query = urllib.urlencode({'q': keywords})

    if num <= 4:
        
        i = 4 - num
        url = googleURL[0] % query
        search_response = urllib.urlopen(url)
        search_results = search_response.read()

        results = json.loads(search_results)

        data = results['responseData']

        hits = data['results']

        for h in hits:
            out.append(h['url'])
        while(i > 0):
            out.pop()
            i = i - 1

            
    else:
        loop = num/4
        loop = loop - 1
        remainder = num%4

        
        url = googleURL[0] % query
        search_response = urllib.urlopen(url)
        search_results = search_response.read()

        results = json.loads(search_results)

        data = results['responseData']

        hits = data['results']

        for h in hits:
            out.append(h['url'])

        i = 1

        while(loop > 0):
            N = 4*i
            url = googleURL[1] %(query, N)
            search_response = urllib.urlopen(url)
            search_results = search_response.read()

            results = json.loads(search_results)

            data = results['responseData']

            hits = data['results']

            for h in hits:
                out.append(h['url'])

            loop = loop - 1
            i = i + 1

        if (remainder > 0):
            i = 4 - remainder
            N = 4*i
            url = googleURL[1] %(query, N)
            search_response = urllib.urlopen(url)
            search_results = search_response.read()

            results = json.loads(search_results)

            data = results['responseData']

            hits = data['results']

            for h in hits:
                out.append(h['url'])
            while(i > 0):
                out.pop()
                i = i - 1

    print 'Top %d google results of %s are:' %(num,keywords), out
    return out
            
