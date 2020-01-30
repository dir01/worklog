Simple python script that I use to track time that I spent at work compared to time I should have spent at work.
It accepts an URL to a Google Sheet that gets populated by IFTTT "When I enter or leave the area" automation.

    $ git clone git@gitlab.com:dir01/worklog.git
    $ virtualenv --python=python3.6 /tmp/env
    $ source /tmp/env/bin/activate
    $ pip install -r worklog/requirements.txt
    $ python3 worklog --url=YOUR_URL --week=su,mo,tu,we --holiday=09.09.18:4 --holiday=10.09.18 --holiday=11.09.18
    $ pytest worklog
