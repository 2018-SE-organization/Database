from html.parser import HTMLParser

comp = lambda f ,g:lambda a:f(g(a))
preslash = lambda xs:xs[:xs.find('/')].strip()
posslash = lambda xs:xs[xs.find('/') + 1:].strip()
quoted = lambda xs: '"' + xs + '"'
cquoted = lambda xs: quoted(xs) + ', '

buff = lambda txt: print(cquoted(txt), end='')
reverse = lambda x: x[::-1]

hField = lambda fd, fn, ed : (lambda data: print(quoted(fd) + ":" + fn(data), end=ed))

buffpre = lambda txt: print(cquoted(preslash(txt)), end='')

splitBy = lambda ch:(lambda xs:xs.split(ch))

rmChrFrom = lambda ch: lambda xs:''.join([x for x in xs if x != ch])

def predMkr(ptag, pattr, func):
    return (lambda tag, attrs: ptag == tag and \
            func(dict(attrs).get(pattr , 'None')))

def isPostfix(ts, os):
    return reverse(ts)[:len(os)] == reverse(os)

def pofixOf(os):
    return lambda ts:isPostfix(ts, os)

class Processer():
    def __init__(self, predfunc, prcsfunc):
        self.guard = False
        self.predfunc = predfunc
        self.prcsfunc = prcsfunc
    def pred(self, tag, attrs):
        if self.predfunc(tag, attrs):
            self.guard = True
    def prcs(self, data):
        if self.guard:
            self.prcsfunc(data)
            self.guard = False

class CourseParser(HTMLParser):

    def __init__(self):

        HTMLParser.__init__(self)
        self.entries = [
#                Processer(predMkr('span', 'id', pofixOf('_coursenumL')), buff),
                Processer(predMkr('span', 'id', pofixOf('_pointL')), hField('point', comp(str, comp(int, float)), ',')),
                Processer(predMkr('span', 'id', pofixOf('_sessionL')), hField("time", quoted, ',')),
#                Processer(predMkr('span', 'id', pofixOf('_placeL')), buff),
#                Processer(predMkr('span', 'id', pofixOf('_MOIL')), buffpre),
#                Processer(predMkr('span', 'id', pofixOf('_department_instituteL')), buff),
#                Processer(predMkr('span', 'id', pofixOf('_volumeL')), buff),
#                Processer(predMkr('span', 'id', pofixOf('_CEL')), buffpre),
#                Processer(predMkr('span', 'id', pofixOf('_kerlL')), buffpre),
                Processer(predMkr('a', 'id', pofixOf('_instructorHL')), hField("inst", comp(str, comp(splitBy('、'), preslash)), ',')),
                Processer(predMkr('a', 'id', pofixOf('_course_nameHL')), hField("cname", comp(quoted, rmChrFrom('"')), '\n')),
                ]

    def handle_starttag(self , tag , attrs):
        for prcser in self.entries:
            prcser.pred(tag, attrs)

        # for course URL
        if tag == 'input' and \
            isPostfix(dict(attrs).get('id' , 'None'), '_schm_tpeIB'):
            print('"url":"http://wa.nccu.edu.tw/qrytor/' + \
                    dict(attrs).get('onclick' , 'None')[24:-16] + '"', end=',') # outline

    def handle_data(self , data):

        for prcser in self.entries:
            prcser.prcs(data)

    def handle_endtag(self , tag):
        pass


if __name__ == "__main__":
    parser = CourseParser()
    print('"coursenum", "instructor", "point", "place", "courseURL", "lang", "depart", "length", "ness", "kernal", "name"')
    for i in range(1, 21):
        parser.feed(open('data/qryScheduleResult.aspx.' + str(i), 'r').read())
