
![tests](https://github.com/tsh/market-analyzer/actions/workflows/python-app.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/tsh/market-analyzer/badge.svg?branch=master)](https://coveralls.io/github/tsh/market-analyzer?branch=master)
![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/tsh/market-analyzer)

# 
YOLO! Donate your money to wall street. Professionally.

## Run
Run from this level, as module separated with dots:
> python3 -m <path.to.the.file>  
 
## Tests

Specific file:
> pytest crawlers/vic/tests/test_idea_parser.py -s
 
All with tag `smoke`:
> pytest -s -m smoke 

All except marked as smoke:
> pytest -s -m "not smoke"

## Installation

- `pip install -r requirements.txt`
- `source setup.sh`
- [non-python deps](provision/README.md)

