[![Build Status](https://travis-ci.org/Doteveryone/BetterJobAdverts.svg?branch=master)](https://travis-ci.org/Doteveryone/BetterJobAdverts)

###Installing and running locally

Clone the repo and install requirements:

```
git clone git@github.com:Doteveryone/BetterJobAdverts.git
cd BetterJobAdverts
virtualenv .
pip install -r requirements.txt
```

To run the website:

```
source bin/activate
python server.py
```

To run the tests:
```
source bin/activate
python tests.py.py
```

To run asset pipeline:
```
gulp
```