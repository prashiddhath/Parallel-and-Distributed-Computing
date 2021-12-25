from mrjob.job import MRJob

import re

class WordCount(MRJob):

   def mapper(self, key, value):
      word_list = value.split()

      for word in word_list:
         yield(word, 1)

   def reducer(self, key, values):
      yield(key, sum(values))

if __name__ == '__main__':
   WordCount.run()
