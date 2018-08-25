import sys
sys.path.insert(0,'tests')
import setup_test

from idor_utils import json

# Loading data
data = json.load('sample.json')
json.save('out.json', data)