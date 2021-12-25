
from mrjob.job import MRJob
from mrjob.step import MRStep

import re
import sys

class AverageMaxDailyTemperatures(MRJob):

   def mapper_max_daily_station_date(self, key, value):
      station = value[4:15]
      date = value[15:23]
      temp = value[87:92]
      q = value[92:93]
      if (temp != "+9999" and re.match("[01459]", q)):
         yield(station+date, int(temp))

   def reducer_max_daily_station_date(self, key, values):
      yield(key, max(values))

   def mapper_average_daily_station_temp(self, key, value):
      station = key[0:11]
      date = key[11:19]
      max_temp = value
      station_day_month = "%s-%s" % (station,date[4:8])
      yield(station_day_month, max_temp)

   def reducer_average_daily_station_temp(self, key, values):
      temp_sum = 0.0
      count = 0
      for val in values:
         temp_sum = temp_sum+val
         count = count + 1
      yield(key, (temp_sum/10.0) / count)

   def steps(self):
      return [
         MRStep(mapper=self.mapper_max_daily_station_date,
               combiner=self.reducer_max_daily_station_date,
               reducer=self.reducer_max_daily_station_date
               )
               ,
         MRStep(mapper=self.mapper_average_daily_station_temp,
               reducer=self.reducer_average_daily_station_temp)
               ]


if __name__ == '__main__':
   AverageMaxDailyTemperatures.run()
