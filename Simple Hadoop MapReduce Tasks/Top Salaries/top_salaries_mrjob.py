from mrjob.job import MRJob
import csv
import sys

class TopSalaries(MRJob):
    
    def mapper(self, key, value):
        entries = csv.reader([value]).__next__()
        try:
            salary_string = entries[5]
            salary = float(salary_string[1:])

            yield ("salary", salary)
        except IndexError:
            for entry in entries:
                sys.stdout.write(entry.encode('utf-8'))
            sys.exit(1)
    
    def reducer(self, key, values):
        out = []
        
        for value in values:
            out.append(value)
         
        out.sort(reverse=True)
        out = out[:10]
        
        yield(key, out)

if __name__ == '__main__':
    TopSalaries.run()
