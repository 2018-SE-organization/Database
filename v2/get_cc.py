from html.parser import HTMLParser

class CodeParser(HTMLParser):

    def __init__(self):

        HTMLParser.__init__(self)
        self.guard = False

    def handle_starttag(self , tag , attrs):
        if tag == 'font':
            attrs = dict(attrs)
            c = lambda a, v: attrs.get(a, '') == v
            if c('size', "3") \
                    and c('color', "#000000") \
                    and c('face', "Times New Roman") :
                self.guard = True

    #<font face="Times New Roman" size="3" color="#000000">350021</font>

    def handle_data(self , data):
        if self.guard:
            if data.isdigit() and len(data) > 3:
                print('0' * (9 - len(data)) + data)
            self.guard = False

    def handle_endtag(self , tag):
        pass

if __name__ == "__main__":
    parser = CodeParser()
    parser.feed(open('1062.html', 'r').read())
