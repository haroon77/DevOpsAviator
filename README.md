# DevOpsAviator
This is a small project which, I have created to automate day to day devops jobs.
This prototype has been designed with the below scope. 

1.	Get a pool of live boxes under DevOps scope. 
2.	Connect to them all and check if any one of the box is running any critical tasks related to production/business/critical testing. 
3.	In case if the box is running a critical process then skip the box and process through other boxes.  For this project I have taken “mysql” server as the critical process for instance. But this can be dynamically altered via the configuration file for the project. See source code hierarchy for config file location.
4.	Any boxes that are not running critical process, bring them offline by sending a broad cast message to all users with a grace period of 5 minutes time, so that they can safely logoff.

<b>How to Use/Test </b><br>

1.	Open settings.conf enter value for config parameter “USER_NAME”
2.	Define any critical process in parameter “CRITICAL_PROC”. Mysql is just set for sample
3.	Open “boxes.txt”, set the boxes name(if DNSed) or IP here, as one for each line
4.	Set Python path as shown below
5.	Go to project root(shown below)
6.	Now execute the directory “Terminator”. Yes of course the directory as given below <br>
    <pre> python ./Terminator </pre>
Note: Pls set PYTHONPATH as below to run the application.<br>
export PYTHONPATH=$PYTHONPATH:/path/to/the/project/DevOpsAviator<br>
<pre><b>Source Code Hierarchy</b>
DevOpsAviator		               =>	Project Root
|______init__.py
|____Config
| |______init__.py
| |____boxes.txt		          =>	List of live boxes
| |____settings.conf		      =>	Global Application settings
|____logs			                =>	Logs Directory
| |____terminator.log		      =>	Log file
|____Terminator		            =>	Main source code
| |____main.py			          =>	Application Executable (Main Module)
|____Tools			              =>	Additional Tools required to run the App
| |______init__.py
| |____EnvManager.py	        =>	Class to auto manage the environment settings needed for this Application.
| |____StatusCodes.py		      =>	Application specific status/error/return codes
| |____Tnlogger.py		        =>	Application specific logger
| |____UtilsManager.py	      =>	Application specific Utility Class 
</pre>	

<b>Dev Notes:</b></br>
  *	DB usage has been avoided here, to reduce the dependency (to run obviously you need them) otherwise we would have used DB on the below instances.</br>
       ➢	The system names to which we need to connect and work has been now read from a flat files. </br>
  *	Code has been followed strict standards to adhere industry development standards </br>
       Eg the below </br>
        •	Loggers with file, function names added during logging. Loggers are rotating by default. So no worry about the size, once it               reaches 2 MB size the log file will be rotated. This is automatically taken care in code through config settings.</br>
        •	Project has its own configuration file, where any dynamic information set in the config file will be applied through out the   project. This has been made automatically to read the concerned files and directory. So we no need to set anything, just set python path as given in the note. Rest code will take care. This is facilitated through a Manager class called EnvManager.( EnvManager.py) and an utils manager(UtilsManager.py) to manage config and other dependent utilities.</br>
       •	Import Sequence, followed per se import rules, as given below</br>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;First import standard libraries</t></br>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Import 3rd party libraries</br>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Import our own dependent modules</br>


*	In this simple project, commands are executed at remote machine, for example getting load average of the remote machine. There are two ways to do that, which are given below<br>
Way 1.	Execute a shell command </br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Connect to the remote machine using SSH and run the shell command, get the stdout and parse it. This is just a straight way of doing it.</br>
Way 2.	Execute a remote python object</br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Connect to the remote machine using SSH and run remote python object(executing piece of python code). This is efficient. But has limitations. We need python to be installed on the target machine. This is preferred if we can write a high performance server. Where we will have full control of the remote execution. </br>
I have shown examples for both cases in my code </br>
<b></br>Code Samples</b></br>
&nbsp;&nbsp;* Way 1 </br>
&nbsp;&nbsp;&nbsp;&nbsp;stdin, stdout, stderr = ssh.exec_command("uptime")</br>
&nbsp;&nbsp;* Way 2</br>
&nbsp;&nbsp;&nbsp;&nbsp;stdin, stdout, stderr = ssh.exec_command("python -c \"import os; load=os.getloadavg(); print load\"")</br>

*	We can do more on this using python remote objects (remotely or pyro libraries) as of now leaving it due to time crunch.

<b>Add ons</b></br>
&nbsp;&nbsp;&nbsp;We can write a separate unit-testing module for this Application. This is open as of now.


