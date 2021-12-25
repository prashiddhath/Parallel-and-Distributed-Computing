
from mrjob.job import MRJob

import re
import sys

class StockAnalysis(MRJob):

   def mapper(self, key, value):
      date, apple_open, ibm_open = value.split(',')
      #print(value, file=sys.stderr)
      year = date[:4]
      month = date[5:7]
      if (month=='10' or month=='11' or month=='12'):
         apple_key = 'apple_%s' % year
         ibm_key = 'ibm_%s' % year
         yield(apple_key, float(apple_open))
         yield(ibm_key, float(ibm_open))
      
   def reducer(self, key, values):
      yield(key, max(values))

if __name__ == '__main__':
   StockAnalysis.run()
