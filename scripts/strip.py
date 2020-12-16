import sys
import os


filename = sys.argv[1]
filename = os.path.abspath(filename)

with open(filename, 'r') as src:
  content = src.read()

with open(filename, 'w') as dest:
  dest.write(content.strip())
