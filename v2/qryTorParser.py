from html.parser import HTMLParser
from urllib.request import urlopen
from urllib.parse import urlencode
from timeMask import timeMask

def insert(xs, g):
    ys = []
    for i, e in enumerate(xs[1:]):
        if not g(e) and g(xs[i]):
            ys.append(' ')
        ys.append(e)
    return ''.join(ys)

def handle(data):
    a, b = data['instructor'].split(' / ')
    data['instructor'] = a.split('、')
    data['instructor_en'] = b.split()
    data['session'] = timeMask(data['session'].split(' / ')[0])
    data['crse_type'] = data['crse_type'].split('/')[0]
    data['place'] = insert(data['place'], lambda e: e in '0123456789').split()

class Handler():
    def __init__(self, tag, attr, pred, prcs):
        self.tag = tag
        self.attr = attr
        self.attrv = ''
        self.guard = False
        self._pred = pred
        self._prcs = prcs
        self.counter = 0
    def pred(self, tag, attrs):
        if self.guard and tag == self.tag:
            self.counter += 1
        if self.tag == tag and \
                self._pred(dict(attrs).get(self.attr, 'None')):
            self.guard = True
            self.attrv = dict(attrs)[self.attr]
    def prcs(self, data):
        if self.guard:
            self._prcs(self.attrv, data.strip())
    def clos(self, tag):
        if self.guard and tag == self.tag:
            if self.counter == 0:
                self.guard = False
            else:
                self.counter -= 1

class Buffer():
    def __init__(self):
        self.dict = {}
    def flush(self):
        xlat = {
                'qryresult0_yy_smtL': 'semester', # 學年/期
                'qryresult0_coursenumL': 'code' , # 科目代碼
                'qryresult0_instructorHL': 'instructor', # 教授
                'qryresult0_pointL': 'point' , # 學分
                'qryresult0_sessionL': 'session', # 時段
                'qryresult0_placeL': 'place', # 地點
                'qryresult0_wayL': 'sel_meth', # 選課方式
                'qryresult0_distance_courseL': 'dist_crse', # 遠距教學
                'qryresult0_MOIL': 'language', # 語言
                'qryresult0_eligibleL': 'ofst_genx', # 可抵通識
                'qryresult0_GECL': 'genx_type', # 通識類別
                'qryresult0_chargesL': 'charge', # 付費
                'qryresult0_auxiliaryL': 'aux', # 擴大輔系
                'qryresult0_department_instituteL': 'depart', # 開課系所
                'qryresult0_volumeL': 'volume', # 1.學期課 2.學年課
                'qryresult0_CEL': 'crse_type', # 修別選必
                'qryresult0_kerlL': 'kernal', # 核心通識
                'qryresult0_course_nameHL': 'crse', # 課程名稱
                'qryresult0_chg_remL': 'chg_info', # 異動資訊
                'qryresult0_noteL': 'note' # 備註
                }
        data = {}
        for title in xlat:
            if title in self.dict:
                data[xlat[title]] = self.dict[title]
            else:
                data[xlat[title]] = 'None'
        handle(data)
        print(data)
        self.dict = {}
    def record(self, title, data):
        if title in self.dict:
            self.dict[title] += data
        else:
            self.dict[title] = data

prefixOf = lambda xs:(lambda ys: ys[:len(xs)] == xs)

class CourseParser(HTMLParser):

    def __init__(self):

        HTMLParser.__init__(self)

        self.entries = \
            [Handler(tag, 'id', prefixOf('qryresult0_'), logger.record) \
            for tag in ['span', 'a']]

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
    parser.feed(open('qryTor/504055022.html', 'r').read())
    logger.flush()
