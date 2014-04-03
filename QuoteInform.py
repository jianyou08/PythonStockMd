from QuoteSource import QuoteListener,QuoteData
import threading
from time import ctime, sleep
import winsound
import string

class PlayThread(threading.Thread):
    def __init__(self, count):
        self.wavfile = ""
        self.loopcount = count
        threading.Thread.__init__(self)
    def playSound(self, wavfile):
        self.wavfile = wavfile
        self.start()
    def run(self):
        count = self.loopcount
        while count > 0 :
            count = count - 1
            self.playSoundOnce()

    def playSoundOnce(self):
        winsound.PlaySound(self.wavfile,winsound.SND_FILENAME)


class QuoteInformer(QuoteListener):
    def __init__(self, stock, cmpPrice = 0.0):
        QuoteListener.__init__(self, 'Inform')
        self.stockid = stock   
        self.cmpPrice = cmpPrice
        self.preClose = 0.0
        self.lastPrice = 0.0
        self.playThread = 0
        self.status = 0

    def OnRecvQuote(self, quoteData):
        if cmp(self.stockid, quoteData.id) == 0 :
            self.preClose = string.atof(quoteData.preClose) 
            if self.cmpPrice == 0.0 :
                self.cmpPrice = string.atof(quoteData.preClose) 
            self.ComparePrice(string.atof(quoteData.lastPrice), string.atof(quoteData.lowPrice), string.atof(quoteData.highPrice))

    def playLowSound(self):
        if self.status != -1:
            self.status = -1
            self.playThread = PlayThread(3)
            self.playThread.playSound("wav\level_up.wav")

    def playHighSound(self):
        if self.status != 1:
            self.status = 1
            self.playThread = PlayThread(3)
            self.playThread.playSound("wav\msg.wav")
            
    def normalArea(self):
        self.status = 0

    def printInfo(self, curper, lowPrice, highPrice) :
        #print "stockid  curper  lastPrice  cmpPrice  preClose  lowPrice  highPrice"
        print "%s  %.3f%%  %.3f  %.3f  pre:%.3f  low:%.3f  high:%.3f  %d" % (self.stockid, curper, self.lastPrice, self.cmpPrice, self.preClose, lowPrice, highPrice, self.status)

    def ComparePrice(self, lastPrice, lowPrice, highPrice): pass

class QuotePercentInformer(QuoteInformer):
    def __init__(self, stock, cmpPrice = '0.0', lowper = '-2', highper = '2'):
        QuoteInformer.__init__(self, stock, string.atof(cmpPrice))
        self.lowper = string.atof(lowper)
        self.highper = string.atof(highper)
            
    def ComparePrice(self, lastPrice, lowPrice, highPrice):
        self.lastPrice = lastPrice
        curper = (self.lastPrice - self.cmpPrice) / self.cmpPrice * 100
        self.printInfo(curper, lowPrice, highPrice)
        if curper <= self.lowper :
            self.playLowSound()
        elif curper >= self.highper :
            self.playHighSound()
        else:
            self.normalArea()

class QuoteDifferenceValueInformer(QuoteInformer):
    def __init__(self, stock, cmpPrice = '0.0', lowdiff = '-1.1', highdiff = '1.1'):
        QuoteInformer.__init__(self, stock, string.atof(cmpPrice))
        self.lowdiff = string.atof(lowdiff)
        self.highdiff = string.atof(highdiff)
            
    def ComparePrice(self, lastPrice, lowPrice, highPrice):
        self.lastPrice = lastPrice
        curper = (self.lastPrice - self.cmpPrice) / self.cmpPrice * 100
        diffv = self.lastPrice - self.cmpPrice
        self.printInfo(curper, lowPrice, highPrice)
        #print "diff:%.3f  lowdiff:%.3f  highdiff:%.3f" % (diffv, self.lowdiff, self.highdiff)
        if diffv <= self.lowdiff :
            self.playLowSound()
        elif diffv >= self.highdiff :
            self.playHighSound()
        else:
            self.normalArea()
        
def testInform():
    d = QuoteData()
    d.stockName = "ETF300"
    d.stockid = "510300"
    d.lastPrice = "2.130"
    d.preClose = "2.108"
    d.openPrice = "2.084"
    d.lowPrice = "2.078"
    d.highPrice = "2.160"
    d.avgPrice = "2.125"
    inform = QuotePercentInformer("510300")
    inform.OnQuoteRecv(d)
    d.lastPrice = "2.530"
    inform.OnQuoteRecv(d);
    sleep(5)
    d.lastPrice = "1.981"
    inform.OnQuoteRecv(d);
    
