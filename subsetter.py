#!/usr/local/bin python

import optparse
import sys
from datetime import *

def subset():
  p = optparse.OptionParser()
  p.add_option('--start', '-s', default="1900", type="int", help="Just aggregate data starting with this year.")
  p.add_option('--end', '-e', default="3000", type="int", help="Just aggregate data up to this year.")
  p.add_option('--limit_rows', '-l', default=None, type="int", help="Just parse a fixed number of rows.")
  p.add_option('--sep', '-p', default="\t", help="Character that splits column in main")
  p.add_option('--fill', '-f', action="store_true", dest="fill", default=False, help="Fill missing months with zeroes.")
  p.add_option('--header', '-d', default=None, help="Specify header from a separate file.")
  p.add_option('--header_sep', default="\t", help="Character to split header row.")
  p.add_option('--country1', default=None, help="Country desired in Actor1CountryCode column.")
  p.add_option('--country2', default=None, help="Country desired in Actor2CountryCode column.")  
  options, arguments = p.parse_args()

  date_ix = None
  ix = 0 

  if options.header: 
    with open(options.header, 'rb') as f:
      headers = f.readline().replace(options.header_sep, " ").rstrip().split()
  else: 
    headers = []
  
  for line in sys.stdin:
    # Get the headers
    tmp_line = line.replace('"','').replace("\n", '').split(options.sep)
    if len(headers) == 0:
      headers = tmp_line 
    if ix==0:
      date_ix = headers.index('SQLDATE')
      actor1_country_code_ix = headers.index('Actor1CountryCode')
      actor2_country_code_ix = headers.index('Actor2CountryCode')
      if not options.header: 
        ix += 1
        continue

    # Parse dates and actors 
    this_date = datetime.strptime(tmp_line[date_ix], "%Y%m%d")
    
    country_1 = tmp_line[actor1_country_code_ix]
    country_2 = tmp_line[actor2_country_code_ix]
    c1 = options.country1 or country_1
    c2 = options.country2 or country_2

    # Does this match our criteria for the subset? 
    if this_date.year >= options.start and this_date.year <= options.end:
    	if country_1==c1 and country_2==c2: 
    		sys.stdout.write(line)

if __name__ == '__main__':
  subset()