#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Sequence
# First import standard libraries
import subprocess
from getpass import getpass
import re



#import 3rd party libraries
import paramiko

#import our own dependent modules
from Tools.UtilsManager import UtilsManager
from Tools.StatusCodes import StatusCodes

from Tools.Tnlogger import get_logger, get_log_file

logger = get_logger()


class Terminator(object):
    def __init__(self):
        self.settings = UtilsManager().get_settings('main')
        if not self.settings:
            logger.error("Error while initializing settings")
            raise "Unable to initialise Settings"

    def get_server_list(self):
        try:
            with open(self.settings['boxes_locator'], 'r') as in_file:
                box_list = [box.replace('\n', '') for box in in_file.readlines()]
                box_list = filter((lambda b: b != ''), box_list)
                logger.debug("Getting list of servers %s", box_list)
        except Exception as err:
            logger.error("Error while opening box list file: %s", err.args)
            return [StatusCodes.ERROR, StatusCodes.ERROR]
        return box_list


    def run_remote_command(self, server_name, cmd):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(server_name, username=self.settings['user_name'], password=getpass())
            logger.debug("Running cmd %s thru SSH on server %s", cmd, server_name)
            stdin, stdout, stderr = ssh_client.exec_command(cmd)
            ssh_cmd_err = stderr.readlines()
            ssh_client.close()
            if ssh_cmd_err:
                logger.error("Error while running cmd=%s, Error=%s", cmd, ssh_cmd_err)
                return (StatusCodes.ERROR, StatusCodes.ERROR, StatusCodes.ERROR)
        except Exception as err:
            logger.error("Unable run remote command in the server. Server=%s, cmd =%s, Error = %s:", server_name, cmd, err.args)
            return (StatusCodes.ERROR, StatusCodes.ERROR, StatusCodes.ERROR)
            ssh_client.close()
        return (stdin, stdout, stderr)

    def check_server_load(self, server_name):
        cmd = "python -c \"import os; load=os.getloadavg(); print load\""
        stdin, stdout, stderr = self.run_remote_command(server_name, cmd)
        if stdout != StatusCodes.ERROR:
            out = stdout.readlines()
            for element in out:
                element = re.sub("[(),]", "", element.strip(), re.UNICODE)
                element = re.split("\s", element, re.UNICODE)
                print "Server %s is currently running %s load" % (server_name, element[0])
                if float(element[0]) > 10.00:
                    logger.error("Target M/C is running under heavy load: %s", element[0])
                    return False
                else:
                    return True


def main():
    try:
        termin = Terminator()
        box_list = termin.get_server_list()
        boxes_terminated = []
        if box_list[0] != StatusCodes.ERROR:
            print "Going to attack these servers: ", box_list
            for box in box_list:
                try:
                    msg = "Trying server {} .....".format(box)
                    print msg
                    logger.info(msg)
                    no_response = subprocess.Popen(["ping", "-c", "1", box], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                    out, err = no_response.communicate()
                    retn_code = no_response.wait()
                    if retn_code == 0:
                        logger.info("Server is up \"%s\"", box)
                        if termin.check_server_load(box):
                            cmd = "ps -A | grep  mysql"
                            #critical_proc = subprocess.call(cmd, stdout=open(get_log_file(), 'a+'), stderr=subprocess.STDOUT, shell=True)
                            stdin, stdout, stderr = termin.run_remote_command(box,cmd)
                            if stdout != StatusCodes.ERROR:
                                remote_proc_list = stdout.readlines()
                                if len(remote_proc_list) > 0:
                                    msg = "Critical process \"%s\" is running on server %s. " % (termin.settings['critical_proc'], box)
                                    msg += "skipping this server"
                                    print msg; logger.warning(msg)
                                    continue
                                else:
                                    msg = "Shutting down the server:" + box
                                    cmd = "sudo shutdown -hk 5 \"Shutting Down…Pls log off in 5 mins. DevOps Automator is taking control of this machine\" "
                                    print msg; logger.info(msg)
                                    stdin, stdout, stderr = termin.run_remote_command(box,cmd)
                                    if stdout != StatusCodes.ERROR:
                                        msg = "Poweroff initiated on server %s. System will go offline in next 5 minutes" % (box)
                                        print msg; logger.info(msg)
                                        boxes_terminated.append(box)
                    else:
                        msg = "Server {}  is not responding. Got error: \n {}".format(box, err)
                        print msg
                        logger.warn(msg)

                except Exception as girr:
                    print "Server is not responding...", girr.args

            if len(boxes_terminated) > 0:
                msg = "List of servers Terminated: " + str(boxes_terminated)
                print msg; logger.info(msg)
            else:
                print "No actions taken"
        else:
            logger.error("SSH execution failed")
    except Exception as girr:
        print girr.args; logger.error(girr.args)




if __name__ == '__main__':
    main()
