import htmllib, formatter

# Reference "How to parse out hyperlinks in Python"  http://cis.poly.edu/cs6913/parsing.txt 

class LinksExtractor(htmllib.HTMLParser): # derive new HTML parser

    def __init__(self, formatter) :        # class constructor
        htmllib.HTMLParser.__init__(self, formatter)  # base class constructor
        self.links = []        # create an empty list for storing hyperlinks

    def start_a(self, attrs) :  # override handler of <A ...>...</A> tags
      # process the attributes
        if len(attrs) > 0 :
            for attr in attrs :
                if attr[0] == "href" :         # ignore all non HREF attributes
                    self.links.append(attr[1]) # save the link info in the list

    def get_links(self) :     # return the list of extracted links
        return self.links

