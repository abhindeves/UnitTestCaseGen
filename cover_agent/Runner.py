import subprocess
import time 
import os
from CustomLogger import CustomLogger


class Runner:
    @staticmethod
    def run_command(test_class: str, maven_path: str):
        logger = CustomLogger.get_logger(__name__)
        logger.info(f"Running command for test class: {test_class} in maven path: {maven_path}")
        
        try:
            os.chdir(maven_path)
            logger.info("Control now in the root directory!!!")
            
            command = f"mvn test -Dtest={test_class}"
            logger.info(f"Executing Junit Test for {test_class}")
            
            result = subprocess.run(command,shell=True,text=True,capture_output=True)
            
        except subprocess.CalledProcessError as e:
            print(f"***************Encountered Error while Executing {test_class}**********\n\n{e.stderr.decode()}")
            exit(1)
        
        return result.stdout,result.stderr,result.returncode
        