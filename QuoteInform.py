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
        self.lowPrice = 0.0
        self.highPrice = 0.0
        self.playThread = 0
        self.level = 0

    def OnRecvQuote(self, quoteData):
        if cmp(self.stockid, quoteData.id) == 0 :
            self.preClose = string.atof(quoteData.preClose)
            newPrice = string.atof(quoteData.lastPrice)
            low = string.atof(quoteData.lowPrice)
            high = string.atof(quoteData.highPrice)            
            if self.cmpPrice == 0.0 :
                self.cmpPrice = string.atof(quoteData.preClose)
            else:    
                self.DoDifference(newPrice, low, high)
            self.lastPrice = newPrice
            self.lowPrice = low
            self.highPrice = high
            self.printInfo()
            
    def DoDifference(self, newPrice, lowPrice, highPrice):pass
            
    def playSound(self, level):
        if self.level != level:
            self.level = level
            self.playThread = PlayThread(3)
            if level < 0:
                self.playThread.playSound("wav\level_up.wav")
            else:
                self.playThread.playSound("wav\msg.wav")
            
    def normalArea(self):
        self.level = 0

    def printInfo(self) :
        curper = (self.lastPrice - self.cmpPrice) / self.cmpPrice * 100
        diffv = self.lastPrice - self.cmpPrice
        print "%s  %.3f%%  %.3f[%.3f]  %.3f  pre:%.3f  l:%.3f  h:%.3f  %d" % (self.stockid, curper, self.lastPrice, diffv, self.cmpPrice, self.preClose, self.lowPrice, self.highPrice, self.level)

class QuotePercentInformer(QuoteInformer):
    def __init__(self, stock, cmpPrice = '0.0', lowper = '-2', highper = '2'):
        QuoteInformer.__init__(self, stock, string.atof(cmpPrice))
        self.lowper = string.atof(lowper)
        self.highper = string.atof(highper)
            
    def DoDifference(self, newPrice, lowPrice, highPrice):
        curper = (self.lastPrice - self.cmpPrice) / self.cmpPrice * 100
        if curper <= self.lowper :
            self.playSound(-1)
        elif curper >= self.highper :
            self.playHighSound(1)
        else:
            self.playSound(0)

class QuoteDifferenceValueInformer(QuoteInformer):
    def __init__(self, stock, cmpPrice = '0.0', lowdiff = '-1.1', highdiff = '1.1'):
        QuoteInformer.__init__(self, stock, string.atof(cmpPrice))
        self.lowdiff = string.atof(lowdiff)
        self.highdiff = string.atof(highdiff)
            
    def DoDifference(self, lastPrice, lowPrice, highPrice):
        diffv = self.lastPrice - self.cmpPrice
        print "%.3f %.3f" % (diffv, self.lowdiff)
        if diffv <= self.lowdiff :
            self.playSound(-1)
        elif diffv >= self.highdiff :
            self.playSound(1)
        else:
            self.playSound(0)

class QuoteDiffValuesInformer(QuoteInformer):
    def __init__(self, stock, lowDiffValues, highDiffVAlues, cmpPrice = '0.0' ):
        QuoteInformer.__init__(self, stock, string.atof(cmpPrice))
        self.lowDiffValues = lowDiffValues
        self.highDiffVAlues = highDiffVAlues
        print self.lowDiffValues
        print self.highDiffVAlues 
            
    def DoDifference(self, lastPrice, lowPrice, highPrice):
        diffv = self.lastPrice - self.cmpPrice
        level = self.ComputeLevel(diffv)
        self.playSound(level)
            
    def ComputeLevel(self, diffPrice):
        if diffPrice < 0:
            i = 0
            for lv in self.lowDiffValues:
                if diffPrice > lv:
                    return i
                i -= 1
        else:
            i = 0
            for lv in self.highDiffVAlues:
                if diffPrice < lv:
                    return i
                i += 1
        return 0

    
