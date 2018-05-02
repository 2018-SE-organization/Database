from html.parser import HTMLParser

buff = lambda txt: print('"' + txt + '"' + ', ', end='')
flush = lambda txt: print('"' + txt + '"')

reverse = lambda x: x[::-1]

def isPostfix(ts, os):
    return reverse(ts)[:len(os)] == reverse(os)

class CourseParser(HTMLParser):

    def __init__(self):

        HTMLParser.__init__(self)
        self.coursename = False
        self.coursenum = False
        self.instructor = False
        self.point = False
        self.session = False
        self.place = False
        self.lang = False
        self.depart = False
        self.length = False
        self.ness = False
        self.kernal = False

    def handle_starttag(self , tag , attrs):

        if tag == 'span':

            iden = dict(attrs).get('id' , 'None')

            if isPostfix(iden, '_coursenumL'):
                self.coursenum = True # course number
            elif isPostfix(iden, '_pointL'):
                self.point = True     # point
            elif isPostfix(iden, '_sessionL'):
                self.session = True
            elif isPostfix(iden, '_placeL'):
                self.place = True
            elif isPostfix(iden, '_MOIL'):
                self.lang = True
            elif isPostfix(iden, '_department_instituteL'):
                self.depart = True
            elif isPostfix(iden, '_volumeL'):
                self.length = True
            elif isPostfix(iden, '_CEL'):
                self.ness = True
            elif isPostfix(iden, '_kerlL'):
                self.kernal = True

        if tag == 'a':
            iden = dict(attrs).get('id' , 'None')
            if isPostfix(iden, '_instructorHL'):
                self.instructor = True  # instructor
            elif isPostfix(iden, '_course_nameHL'):
                self.coursename = True  # course name

        if tag == 'input' and \
            isPostfix(dict(attrs).get('id' , 'None'), '_schm_tpeIB'):
            buff("http://wa.nccu.edu.tw/qrytor/" + \
                    dict(attrs).get('onclick' , 'None')[24:-16]) # outline

    def handle_data(self , data):
        if self.coursenum:
            buff(data)
            self.coursenum = False
        if self.instructor:
            buff(data)
            self.instructor = False
        if self.point:
            buff(data)
            self.point = False
        if self.place:
            buff(data)
            self.place = False
        if self.lang:
            buff(data)
            self.lang = False
        if self.depart:
            buff(data)
            self.depart = False
        if self.length:
            buff(data)
            self.length = False
        if self.ness:
            buff(data)
            self.ness = False
        if self.kernal:
            buff(data)
            self.kernal = False
        if self.coursename:
            flush(data)
            self.coursename = False

    def handle_endtag(self , tag):
        pass


if __name__ == "__main__":
    parser = CourseParser()
    print('"coursenum", "instructor", "point", "place", "courseURL", "lang", "depart", "length", "ness", "kernal", "name"')
    for i in range(1, 21):
        parser.feed(open('qryScheduleResult.aspx.' + str(i), 'r').read())
