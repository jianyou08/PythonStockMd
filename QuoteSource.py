import urllib
import urllib2
import threading
from time import ctime, sleep

class QuoteData:
    def __init__(self):
        self.id = ''
        self.rawLine = ''
        #sorted with sina interface
        self.name = ''
        self.openPrice = ''
        self.preClose = ''
        self.lastPrice = ''
        self.highPrice = ''
        self.lowPrice = ''
        self.buyPrice = ''
        self.sellPrice = ''
        self.tradeValume = ''
        self.tradeTurnover = ''
        self.buy1Volume = ''
        self.buy1Price = ''
        self.buy2Volume = ''
        self.buy2Price = ''
        self.buy3Volume = ''
        self.buy3Price = ''
        self.buy4Volume = ''
        self.buy4Price = ''
        self.buy5Volume = ''
        self.buy5Price = ''
        self.sell1Volume = ''
        self.sell1Price = ''
        self.sell2Volume = ''
        self.sell2Price = ''
        self.sell3Volume = ''
        self.sell3Price = ''
        self.sell4Volume = ''
        self.sell4Price = ''
        self.sell5Volume = ''
        self.sell5Price = ''
        self.date = ''
        self.time = ''
    
    def toString(self):
        return self.name + '(' + self.id + ')' \
            + ', openPrice=' + self.openPrice \
            + ', preClose=' + self.preClose \
            + ', lastPrice=' + self.lastPrice  \
            + ', highPrice=' + self.highPrice  \
            + ', lowPrice=' + self.lowPrice  \
            + ', buyPrice=' + self.buyPrice  \
            + ', sellPrice=' + self.sellPrice  \
            + ', tradeValume=' + self.tradeValume  \
            + ', buy1Volume=' + self.buy1Volume  \
            + ', buy1Price=' + self.buy1Price \
            + ', buy2Volume=' + self.buy2Volume \
            + ', buy2Price=' + self.buy2Price \
            + ', buy3Volume=' + self.buy3Volume \
            + ', buy3Price=' + self.buy3Price \
            + ', buy4Volume=' + self.buy4Volume \
            + ', buy4Price=' + self.buy4Price \
            + ', buy5Volume=' + self.buy5Volume \
            + ', buy5Price=' + self.buy5Price \
            + ', sell1Volume=' + self.sell1Volume  \
            + ', sell1Price=' + self.sell1Price  \
            + ', sell2Volume=' + self.sell2Volume  \
            + ', sell2Price=' + self.sell2Price  \
            + ', sell3Volume=' + self.sell3Volume  \
            + ', sell3Price=' + self.sell3Price  \
            + ', sell4Volume=' + self.sell4Volume  \
            + ', sell4Price=' + self.sell4Price  \
            + ', sell5Volume=' + self.sell5Volume  \
            + ', sell5Price=' + self.sell5Price  \
            + ', date=' + self.date  \
            + ', time=' + self.time
    
    @staticmethod
    def csvHead():
        head = 'name,id,time,openPrice,preClose,lastPrice,highPrice,lowPrice,buyPrice,sellPrice,tradeValume,tradeTurnover,buy1Volume ,buy1Price,buy2Volume,buy2Price,buy3Volume,buy3Price,buy4Volume,buy4Price,buy5Volume,buy5Price,sell1Volume,sell1Price,sell2Volume,sell2Price,sell3Volume,sell3Price,sell4Volume,sell4Price,sell5Volume,sell5Price,date'
        return head
        
    def toCSVString(self):
        return '\n' + self.name \
            + ',' + self.id  \
            + ',' + self.time \
            + ',' + self.openPrice \
            + ',' + self.preClose \
            + ',' + self.lastPrice  \
            + ',' + self.highPrice  \
            + ',' + self.lowPrice  \
            + ',' + self.buyPrice  \
            + ',' + self.sellPrice  \
            + ',' + self.tradeValume  \
            + ',' + self.tradeTurnover \
            + ',' + self.buy1Volume  \
            + ',' + self.buy1Price \
            + ',' + self.buy2Volume \
            + ',' + self.buy2Price \
            + ',' + self.buy3Volume \
            + ',' + self.buy3Price \
            + ',' + self.buy4Volume \
            + ',' + self.buy4Price \
            + ',' + self.buy5Volume \
            + ',' + self.buy5Price \
            + ',' + self.sell1Volume  \
            + ',' + self.sell1Price  \
            + ',' + self.sell2Volume  \
            + ',' + self.sell2Price  \
            + ',' + self.sell3Volume  \
            + ',' + self.sell3Price  \
            + ',' + self.sell4Volume  \
            + ',' + self.sell4Price  \
            + ',' + self.sell5Volume  \
            + ',' + self.sell5Price  \
            + ',' + self.date

    def Print(self):
        print self.toString()

class QuoteListener:
    def __init__(self, name):
        self.name = name
    def getName(self):
        return self.name  
    def OnRecvQuote(self, quoteData):pass
    
class QuotePrinter(QuoteListener):
    def __init__(self):
        QuoteListener.__init__(self, 'Printer')

    def OnRecvQuote(self, quoteData):
        quoteData.Print()

class QuoteSource:
    def __init__(self, stocks):
        self.stocks = stocks
        self.listeners = []
        
    def addListener(self, listener):
        self.listeners.append(listener)
        
    def notifyListeners(self, quoteData):
        for lst in self.listeners :
            #print lst.getName()
            lst.OnRecvQuote(quoteData)
        
    def queryStock(self):pass

class QuoteSourceQtimg(QuoteSource):
    def queryStock(self):    
        host="http://qt.gtimg.cn/r=0.9392363841179758&q="
        url = host + self.stocks
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        
        d = QuoteData()
        for line in res.split(';'):
            #print line
            if len(line) < 50 :
                continue
            info = line[12: len(line)-2]
            self.notifyListeners(d)
            vargs = info.split('~')
            #print vargs
            d.name = vargs[1]
            d.stockid = vargs[2]
            d.lastPrice = vargs[3]
            d.preClose = vargs[4]
            d.openPrice = vargs[5]
            d.lowPrice = ''
            d.highPrice = ''
            d.avgPrice = ''
            self.notifyListeners(d)

class QuoteSourceSina(QuoteSource):
    def queryStock(self):    
        host="http://hq.sinajs.cn/list="
        url = host + self.stocks
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        
        qd = QuoteData()
        for line in res.split('\n'):
            #print line
            if len(line) < 50 :
                continue
            stkid = line[13: 19]
            info = line[21:len(line)-2]
            vargs = info.split(',')
            #print vargs
            qd.id = stkid
            qd.rawline = info
            qd.name = vargs[0]
            qd.openPrice = vargs[1]
            qd.preClose = vargs[2]
            qd.lastPrice = vargs[3]
            qd.highPrice = vargs[4]
            qd.lowPrice = vargs[5]
            qd.buyPrice = vargs[6]
            qd.sellPrice = vargs[7]
            qd.tradeValume = vargs[8]
            qd.tradeTurnover = vargs[9]
            qd.buy1Volume = vargs[10]
            qd.buy1Price = vargs[11]
            qd.buy2Volume = vargs[12]
            qd.buy2Price = vargs[13]
            qd.buy3Volume = vargs[14]
            qd.buy3Price = vargs[15]
            qd.buy4Volume = vargs[16]
            qd.buy4Price = vargs[17]
            qd.buy5Volume = vargs[18]
            qd.buy5Price = vargs[19]
            qd.sell1Volume = vargs[20]
            qd.sell1Price = vargs[21]
            qd.sell2Volume = vargs[22]
            qd.sell2Price = vargs[23]
            qd.sell3Volume = vargs[24]
            qd.sell3Price = vargs[25]
            qd.sell4Volume = vargs[26]
            qd.sell4Price = vargs[27]
            qd.sell5Volume = vargs[28]
            qd.sell5Price = vargs[29]
            qd.date = vargs[30]
            qd.time = vargs[31]
            
            self.notifyListeners(qd)

class QuoteThread(threading.Thread):
    def __init__(self, source, intervalSecs = 3):
        self.source = source
        self.interval = intervalSecs
        self.threadRunning = False
        threading.Thread.__init__(self)

    def run(self):
        print 'StockQuote run'
        self.threadRunning = True;
        while self.threadRunning:
            self.source.queryStock()
            sleep(self.interval)

    def stop(self):
        print 'StockQuote stop'
        self.threadRunning = False;

        
        
