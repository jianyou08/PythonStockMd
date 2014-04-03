from QuoteSource import QuoteListener,QuoteData
import string
import time
from time import ctime, sleep
import random

class QuoteSaveToCSV(QuoteListener):
    def __init__(self, stock):
        QuoteListener.__init__(self, 'Saver')
        self.stockid = stock
        self.filename = stock + time.strftime('%Y%m%d.csv',time.localtime(time.time()))  
        self.outfile = open(self.filename, 'a+')
        self.outfile.write(QuoteData.csvHead())
        self.outfile.close()

    def OnRecvQuote(self, quoteData):
        if cmp(self.stockid, quoteData.id) == 0 :
            self.outfile = open(self.filename, 'a+')
            self.outfile.write(quoteData.toCSVString())
            self.outfile.close()

#def testQuoteSaveToCSV():
if __name__ == '__main__':
    d = QuoteData()
    d.name = "ETF300"
    d.id = "510300"
    d.lastPrice = "2.130"
    d.preClose = "2.108"
    d.openPrice = "2.084"
    d.lowPrice = "2.078"
    d.highPrice = "2.160"
    d.date = "2014-04-03"
    d.time = "15:05:03"
    inform = QuoteSaveToCSV("510300")
    inform.OnRecvQuote(d)
    d.lastPrice = "2.530"
    inform.OnRecvQuote(d);
    sleep(5)
    d.lastPrice = "1.981"
    inform.OnRecvQuote(d);
    
