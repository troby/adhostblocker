#!/usr/bin/env python2.7
import re, requests, sys, os, tempfile

# bad hosts taken from someonewhocares.org
url = 'http://someonewhocares.org/hosts/'

def get_blacklist():
  # quietly die if request cannot be made
  try:
    blacklist = requests.get(url)

    if blacklist.status_code != 200:
      sys.exit(0)
  except:
    sys.exit(0)

  bad_hosts = []
  for line in blacklist.text.split('\n'):
    if re.match(r'^127.0.0.1', line):
      bad_hosts.append(line)
  if len(bad_hosts) == 0:
    sys.exit(0)
  return bad_hosts

def save_hosts(bad_hosts):
  (fd, filename) = tempfile.mkstemp(prefix='hosts-', dir=os.path.abspath('.'))
  for host in bad_hosts:
    os.write(fd, host + '\n')
  os.close(fd)

def main():
  bad = get_blacklist()
  save_hosts(bad)

if __name__ == '__main__':
  main()
