Use project as a tool for automatic testing of web, desktop and other applications.

1. Download and install the latest version of Python 3.x

2. Before the start in UNIX launch `terminal` and execute command `cd /home/<username>/AutoTestsTemplate/src`. 
   
   In Windows launch `cmd`  and execute command `cd D:\AutoTestsTemplate\src`

3. In cmd execute "pip install -r requirements.txt" to install packages used in the project.

4. Go to https://www.seleniumhq.org/download/ and download the latest versions of chromedriver.exe, geckodriver.exe, IEDriverServer.exe.

   In Windows: save them in `C:\Program Files\Python36\Scripts`, write `C:\Program Files\Python36\Scripts` in  environmental variables.
   
   In Linux: save chromedriver, geckodriver, IEDriverServer to `/usr/bin/`

5. For launching tests: 
	- Go to your directory with tests, e.g. `D:\AutoTestsTemplate\src\tests` or `/home/<username>/AutoTestsTemplate/src`
	- Execute command `python run_tests.py` or just click on `run_autotests.bat` (in Windows), which actually execute the same command `python run_tests.py`.

6. Project structure:

	`common.py`   - base file with methods called in the tests.
	
	`conftest.py` - configuration file with imported modules, logging, importing test data (json, mysql), selenium webdriver (chrome, mozilla, ie), preconditions; postconditions (screenshots after every test case, test reports, email notifications, removing old logs, reports and screenshots).
	
       |
        -> tests
        -> screenshots
        -> report
        -> modules (self-made)
        -> logs
        -> data (images, logins-passwords, whatever)