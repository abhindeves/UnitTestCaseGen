import datetime
import os
import pandas as pd
import json
# import wandb

from CustomLogger import CustomLogger
from UnitTestGenerator import UnitTestGenerator
from Runner import Runner

class CoverAgent:
    def __init__(self, args):
        self.args = args
        self.logger = CustomLogger.get_logger(__name__)
        self.maven_file_path = args.maven_file_path
        self.logger.info("Arguments passed to Cover Agent", extra={'argument': args})
        self.logger.info("Validating source file path", extra={'source_file_path': args.source_file_path})
        
        self._validate_paths(args.source_file_path,type='file')
        
        self._validate_paths(args.destination_file_path,type='folder')
        
        self.logger.info("Initializing unit test generator", extra={'model': args.model})
        self.test_gen = UnitTestGenerator(
            source_file_path=args.source_file_path,
            test_file_path=args.destination_file_path,
            maven_file_path = args.maven_file_path,
            llm_model=args.model,
        )
        self.logger.info("Unit test generator initialized")
        
        

    def _validate_paths(self,path: str,type: str):
        
        if type == 'file':
            if not os.path.isfile(path):
                raise FileNotFoundError(f"Source file not found at {path}")
            
            file_name = path.split('\\')[-1]
            file_type = file_name.split('.')[-1]
            
            if file_type != 'java':
                raise TypeError(f"You Provided {file_name} which is not a java file, please provide Java Code")
            self.logger.info(f"Destination file found at {path}")
            
        elif type == 'folder':
            if not os.path.isdir(path):
                raise FileNotFoundError(f"Test Folder not found at {path}")
            
            if len(os.listdir(path)) != 0:
                self.logger.info("Some files are already present in the given destination file")
                list_of_code_already_present = os.listdir(path)
                print("\nList of file already present")
                print(list_of_code_already_present)
                print("\nPlease ceck the above files and clear it from the destination file or provide another file")
                print(f"Destination Given: {path}")
                exit(-1)
            self.logger.info(f'Test Folder found at {path}')
            

    def run(self):
        self.logger.info("Starting the run", extra={'timestamp': datetime.datetime.now().isoformat()})
        self.logger.info("Initializing Basic Test Suite generation")
        # Loop until desired coverage is reached or maximum iterations are met
        
        generated_tests_dict = self.test_gen.generate_basic_test_suite(max_tokens=4096) 
        with open('generated_tests.json', 'w') as file:
            json.dump(generated_tests_dict, file, indent=4)
            
        # print(generated_tests_dict)
        code_list = [{}]
        test_number = 1
        for generated_test in generated_tests_dict.get('new_tests',[]):
            test_name = generated_test.get('test_name')
            test_class_name = generated_test.get('test_class')
            temp_code_dict = self.test_gen.validate_test(generated_test,test_class_name,test_name)
            code_list.append(temp_code_dict)
            self.logger.info(f"{test_name} added to code_list")
            test_number += 1
        
        self.logger.info("All code added to code_list")
        
        pass_test_list = [junit_test for junit_test in code_list if junit_test.get('exit_code') == 0]
        self.logger.info(f"{len(pass_test_list)} Test Passed")
        fail_test_list = [junit_test for junit_test in code_list if junit_test.get('exit_code') != 0]
        if fail_test_list == [{}]:
            self.logger.info("0 Test Failed")
        else:
            self.logger.info(f"{len(fail_test_list)} Test Failed")
        
        
        self.logger.info('Calling combine_pass_test function to pass all the sucess test case')
        
        combined_response = self.test_gen.combine_pass_test(pass_test_list)
        
        final_test_name = self.test_gen.write_final_test(combined_response)
        
        
        stdout, stderr, exit_code = Runner.run_command(final_test_name, self.maven_file_path)
        self.test_gen.display_result(final_test_name,exit_code,stderr,stdout)
        

    
        self.logger.info('Flow returned to CoverAgent run module')
        self.logger.info('End the Run Function')
        
        

        
        

        
 