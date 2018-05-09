from html.parser import HTMLParser
from urllib.request import urlopen

def predMkr(ptag, pattr, func):
    return (lambda tag, attrs: ptag == tag and \
            func(dict(attrs).get(pattr , 'None')))

class Processer():
    def __init__(self, tag, predfunc, prcsfunc):
        self.tag = tag
        self.guard = False
        self.predfunc = predfunc
        self.prcsfunc = prcsfunc
        self.counter = 0
    def pred(self, tag, attrs):
        if self.guard and tag == self.tag:
            self.counter += 1
        if self.predfunc(tag, attrs):
            self.guard = True
    def prcs(self, data):
        if self.guard and data.strip():
            self.prcsfunc(data.strip())
    def clos(self, tag):
        if self.guard and tag == self.tag:
            if self.counter == 0:
                self.guard = False
            else:
                self.counter -= 1

class Buffer():
    def __init__(self):
        self.list = []
    def flush(self):
        # process, print
        data = []
        title = ['course_zh', 'course_en', 'course_type', 'point', 'depart', 'instructor', 'condition', 'time', 'url']
        select = [0,1,2,4,10,12,14,16,18]
        data = [r \
                for (i, r) \
                in enumerate(self.list) \
                if i in select]

        print({t : d for (t, d) in zip (title, data)})
        self.list.clear()
    def record(self, data):
        self.list.append(data)

class CourseParser(HTMLParser):

    def __init__(self):

        eq2str = lambda xs:(lambda ys: xs == ys)

        HTMLParser.__init__(self)

        self.entries = [
                Processer('span', predMkr('span', 'id', eq2str('CourseName')), logger.record),
                Processer('span', predMkr('span', 'id', eq2str('CourseNameEn')), logger.record),
                Processer('div', predMkr('div', 'class', eq2str('row text-center sylview--mtop')), logger.record),
                Processer('div', predMkr('div', 'class', eq2str('panel-body')), logger.record),
                ]

    def handle_starttag(self , tag , attrs):
        for prcser in self.entries:
            prcser.pred(tag, attrs)

    def handle_data(self , data):
        for prcser in self.entries:
            prcser.prcs(data)

    def handle_endtag(self , tag):
        for prcser in self.entries:
            prcser.clos(tag)

if __name__ == "__main__":
    logger = Buffer()
    parser = CourseParser()
    codes = open('code.txt', 'r').read().split()
    for code in codes[:3]:
        num = code[:6]
        gop = code[6:8]
        s = code[8:9]
        url = 'http://newdoc.nccu.edu.tw/teaschm/1062/schmPrv.jsp-yy=106&smt=2&num=' + num + '&gop=' + gop + '&s=' + s + '.html'
        parser.feed(urlopen(url).read().decode('utf-8'))
        logger.record(url)
        logger.flush()
