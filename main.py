from QuoteSource import QuoteThread, QuoteSourceSina, QuoteSourceQtimg, QuotePrinter, QuoteData
from QuoteInform import *
from QuoteSaver import QuoteSaveToCSV
from time import ctime, sleep
import threading, signal
import string


def runNoThread(stockids):
    s = QuoteSourceSina(stockids)
    #s = QuoteSourceQtimg(stockids)
    #s.addListener(QuotePrinter())
    #s.addListener(QuoteDifferenceValueInformer('510050', '0.0', '-0.008', '0.005'))
    s.addListener(QuoteSaveToCSV('510050'))
    s.addListener(QuoteDiffValuesInformer('510050', [-0.009,-0.019,-0.029], [0.009, 0.019, 0.029], '0.0'))
    try:
        while True:
            s.queryStock()
            sleep(3)
    except KeyboardInterrupt, e:
        print 'StockQuote stop'


is_exit = False
def mainloop(s):
    global is_exit
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt, e:
        s.stop()

def runWithThread(stockids):
    s = QuoteSourceSina(stockids)
    #s = QuoteSourceQtimg(stockids)
    s.addListener(QuotePrinter())
    #s.addListener(QuotePercentInformer('510300'))
    s.addListener(QuoteDifferenceValueInformer('510050', '1.485', '-0.008', '0.005'))
    thread = QuoteThread(s)
    thread.setDaemon(True)
    thread.start()
    mainloop(thread)

        
if __name__ == '__main__':
    runNoThread('sh600006,sh510050')
    #runWithThread('sh000001,sh510050')

        
    