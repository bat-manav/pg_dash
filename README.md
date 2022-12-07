# pg_dash
terminal based postgres monitoring script  with live refresh .

NOTE - > This script is tested against RHEL only. 

PRE-REQUISITES:

1. Install python3 and below additional modules.

example - > /usr/bin/python3 -m pip install rich

import rich
import datetime
import psutil
import pyfiglet
import os
import psycopg2

2. Update the connect.py file with connection details.


3. Run the python script as below .

/usr/bin/python3 pg_dash_v1.py


<a href="https://asciinema.org/a/0YrjtP1e8ao7gPE10tH3rELGt" target="_blank"><img src="https://asciinema.org/a/0YrjtP1e8ao7gPE10tH3rELGt.svg" /></a>
