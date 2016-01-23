#!/usr/local/bin/python2.7
import re, requests, sys, os

# bad hosts taken from someonewhocares.org
url = 'http://someonewhocares.org/hosts/'
output = 'hosts'

try:
  blacklist = requests.get(url)

  if blacklist.status_code != 200:
    sys.exit(0)
except:
  sys.exit(0)

if not os.path.isfile(output):
  fh = open(output, 'w')
  for line in blacklist.text.split('\n'):
    if re.match(r'^127.0.0.1', line):
      fh.write(line + '\n')
  fh.close()
