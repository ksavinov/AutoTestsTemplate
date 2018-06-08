#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime

print("\nYou ran the first test suite.")
os.system('pytest --html=../report/report-{}.html -v tests_first.py'.format(datetime.strftime(datetime.now(), '%Y-%m-%d__%H_%M_%S%f')))
