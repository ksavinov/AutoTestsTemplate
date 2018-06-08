0. Download and install the latest version of Python 3.x

1. Before the start in cmd go to folder src, e.g. "cd D:\YourProject\src"

2. In cmd execute "pip install -r requirements.txt" to install packages used in the project.

3. Go to https://www.seleniumhq.org/download/ and download the latest versions of chromedriver.exe, geckodriver.exe, IEDriverServer.exe,
   Save them in C:\Program Files\Python36\Scripts
   Write "C:\Program Files\Python36\Scripts" in  environmental variables.

4. For launching tests: 
	- Go to your directory with tests, e.g. D:\YourProject\src\tests
	- In cmd execute "python run_tests.py" or just click on run_autotests.bat, which actually execute the same command "python run_tests.py".

5. Project structure:
	common.py   - base file with methods called in the tests.
	conftest.py - configuration file with imported modules, logging, importing test data (json, mysql), selenium webdriver (chrome, mozilla, ie), preconditions; postconditions (screenshots after every test case, test reports, email notifications, removing old logs, reports and screenshots).
		|
		|
		-> tests
		-> screenshots
		-> report
		-> modules (self-made)
		-> logs
		-> data (images, logins-passwords, whatever)