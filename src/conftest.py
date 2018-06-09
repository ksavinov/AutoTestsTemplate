#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pywinauto
import json
import os
import sys
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from smtplib import SMTP_SSL
import logging
from datetime import datetime
import MySQLdb

sep='\uA789' # instead of ":", which is not supported in Windows file names
now = lambda: datetime.now().strftime("%Y-%m-%d_%H:%M:%S").replace(':', sep) # ISO_8601: YYYY-MM-DD

# set up logging to file
today = lambda: datetime.now().strftime("%Y-%m-%d") # ISO_8601: YYYY-MM-DD
LOG_FILENAME = os.path.abspath(os.path.join(os.getcwd(), '..', 'logs', 'log_-%s.log' % today()))
logging.basicConfig(
filename=LOG_FILENAME,
format='[LINE:%(lineno)d] %(asctime)s %(levelname)s %(message)s',
datefmt='%Y-%m-%d %H:%M:%S',
level=logging.DEBUG)

log = logging.getLogger('test.test')

# if importing test data from json:
data_file = open(os.path.abspath(os.path.join(os.getcwd(), '..', 'data', 'test_users.json')),
                 encoding="utf8")
data = json.loads(data_file.read())

# select user login from db
try:
    conn = MySQLdb.connect(host="localhost", user="username",
                           passwd="password", db="dbname", charset='utf8')
except MySQLdb.Error as err:
    print("Connection error: {}".format(err))
    conn.close()

user_login = "SELECT `login` FROM `test_users` WHERE id = 1"
try:
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(user_login)
    data = cur.fetchmany()
except MySQLdb.Error as err:
    log.debug("Query error: {}".format(err))
login_data = str(data)

# select user password from db
user_login = "SELECT `password` FROM `test_users` WHERE id = 1"
try:
    cur = conn.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(user_login)
    data = cur.fetchmany()
except MySQLdb.Error as err:
    log.debug("Query error: {}".format(err))
passwd_data = str(data)

class FirefoxDriverManagerProxy(object):

    def __init__(self):
        self._instance = None

    def start(self, type='ff'):
        # implement logic to create instance depends on condition
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy_type', 1)
        profile.set_preference('network.proxy.http', "27.22.120.163")
        profile.set_preference('network.proxy.http_port', 53281)
        profile.update_preferences()
        self._instance = webdriver.Firefox(firefox_profile=profile)
        return self._instance

    @property
    def instance(self):
        if not self._instance:
            self.start()
        return self._instance

    def stop(self):
        self._instance.quit()
        self._instance = None

class FirefoxDriverManager(object):

    def __init__(self):
        self._instance = None

    def start(self, type='ff'):
        profile = FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.dir", os.path.abspath(os.path.join(os.getcwd())))
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        profile.set_preference("pdfjs.disabled", True)
        
        # Инициализация браузера Mozilla Firefox
        self._instance = webdriver.Firefox(profile)
        return self._instance

    @property
    def instance(self):
        if not self._instance:
            self.start()
        return self._instance

    def stop(self):
        self._instance.quit()
        self._instance = None        
        
class ChromeDriverManager(object):

    def __init__(self):
        self._instance = None

    def start(self, type='ff'):
        self._instance = webdriver.Chrome()
        return self._instance

    @property
    def instance(self):
        if not self._instance:
            self.start()
        return self._instance

    def stop(self):
        self._instance.quit()
        self._instance = None        

class IEDriverManager(object):

    def __init__(self):
        self._instance = None


    def start(self, type='ff'):
        caps = DesiredCapabilities.INTERNETEXPLORER
        caps['ignoreProtectedModeSettings'] = True
        self._instance = webdriver.Ie(capabilities=caps)
        return self._instance

    @property
    def instance(self):
        if not self._instance:
            self.start()
        return self._instance

    def stop(self):
        self._instance.quit()
        self._instance = None

@pytest.fixture(scope="module") # scope="function" / scope="module" / scope="class"
def driver():
    return ChromeDriverManager()

@pytest.fixture(scope="module")
def mozilla_driver():
    return FirefoxDriverManager()
    
@pytest.fixture(scope="module")
def ie_driver():
    return IEDriverManager()

@pytest.fixture(scope="class")
def manage_driver(request, driver):
    driver.start()
    yield
    driver.stop()

@pytest.fixture(scope="class")
def manage_mozilla_driver(request, mozilla_driver):
    mozilla_driver.start()
    yield
    mozilla_driver.stop()  

@pytest.fixture(scope="class")
def manage_ie_driver(request, ie_driver):
    ie_driver.start()
    yield
    ie_driver.stop()

@pytest.fixture(scope="class")
def login_driver(request, driver, manage_driver):     # Preconditions for Chrome Driver
    # maximize window
    driver.instance.set_window_size(1920, 1080)
    driver.instance.maximize_window()

@pytest.fixture(scope="class")
def login_mozilla(request, mozilla_driver, manage_mozilla_driver):  # Preconditions for Chrome Driver
    mozilla_driver.instance.set_window_size(1920, 1080)
    mozilla_driver.instance.maximize_window()

@pytest.fixture(scope="class")
def login_ie(request, ie_driver, manage_ie_driver):  # Preconditions for Chrome Driver
    ie_driver.instance.set_window_size(1920, 1080)
    ie_driver.instance.maximize_window()

screenshot_list = []

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    global report
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        if 'driver' in item._fixtureinfo.name2fixturedefs:
            driver = item._fixtureinfo.name2fixturedefs['driver'][-1
            ].cached_result[0]
        elif 'mozilla_driver' in item._fixtureinfo.name2fixturedefs:
            driver = item._fixtureinfo.name2fixturedefs['mozilla_driver'][-1
            ].cached_result[0]
        elif 'ie_driver' in item._fixtureinfo.name2fixturedefs:
            driver = item._fixtureinfo.name2fixturedefs['ie_driver'][-1
            ].cached_result[0]

        # always add url to report
        extra.append(pytest_html.extras.url(driver.instance.current_url))

        filename = (os.path.abspath(os.path.join(os.getcwd(), '..', 'screenshots', 'screen_{}.png'.format(datetime.strftime(datetime.now(), '%Y-%m-%d__%H_%M_%S%f')))))
        driver.instance.get_screenshot_as_file(filename)
        
        extra.append(pytest_html.extras.image(filename))
        extra.append(pytest_html.extras.html('<div>Additional HTML</div>'))
        report.extra = extra

def pytest_sessionfinish(session, exitstatus):
    current_time = time.time()
    # delete screenshots created over 31 days ago
    os.chdir('..')
    os.chdir('screenshots')
    for f in os.listdir():
        creation_time = os.path.getctime(f)
        if (current_time - creation_time) // (24 * 3600) > 31:
            os.unlink(f)
            log.debug('{} deleted'.format(f))

    # delete logs created over 31 days ago
    os.chdir('..')
    os.chdir('logs')
    for f in os.listdir():
        creation_time = os.path.getctime(f)
        if (current_time - creation_time) // (24 * 3600) > 31:
            os.unlink(f)
            log.debug('{} deleted'.format(f))

    # delete reports created over 31 days ago
    os.chdir('..')
    os.chdir('report')
    for f in os.listdir():
        creation_time = os.path.getctime(f)
        if (current_time - creation_time) // (24 * 3600) > 31:
            os.unlink(f)
            log.debug('{} deleted'.format(f))

    # send notifications to e-mail about FAILED and PASSED test suites
    if exitstatus != 0:
        m = MIMEMultipart('alternative')
        m['From'] = 'your_mail'
        m['To'] = 'receivers'
        m['Subject'] = 'Your tests FAILED'
        report_name = str(report)[12:-1]
        test_suite = report_name.split('::')[1]
        body = 'See more: \\path' + '<br><br>' + 'Test suite: ' + test_suite
        m.attach(MIMEText(body.encode('utf-8'), 'html', 'utf-8'))
        mail = smtplib.SMTP('mail_server_address', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('login', 'password')
        mail.sendmail(m['From'], m['To'].split(";"), m.as_string())
        mail.close()
    else:
        m = MIMEMultipart('alternative')
        m['From'] = 'your_mail'
        m['To'] = 'receivers'
        m['Subject'] = 'Your tests PASSED'
        report_name = str(report)[12:-1]
        test_suite = report_name.split('::')[1]
        body = 'See more: \\path' + '<br><br>' + 'Test suite: ' + test_suite
        m.attach(MIMEText(body.encode('utf-8'), 'html', 'utf-8'))
        mail = smtplib.SMTP('mail_server_address', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('login', 'password')
        mail.sendmail(m['From'], m['To'].split(";"), m.as_string())
        mail.close()