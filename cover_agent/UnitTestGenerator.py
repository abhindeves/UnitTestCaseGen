import datetime
import logging
import os
import re
import json
from wandb.sdk.data_types.trace_tree import Trace
from tabulate import tabulate
import pandas as pd

from CustomLogger import CustomLogger
from PromptBuilder import PromptBuilder
from AICaller import AICaller
from utils import load_yaml
from Runner import Runner





class UnitTestGenerator:
    def __init__(self,source_file_path: str,test_file_path: str,maven_file_path: str,llm_model: str):
        self.logger = CustomLogger.get_logger(__name__)
        # Class variables
        self.test_file_path = test_file_path
        self.source_file_path = source_file_path
        self.maven_file_path = maven_file_path
        self.llm_model = llm_model
        
        self.ai_caller = AICaller(model=self.llm_model)
        self.total_input_token_count = 0
        self.total_output_token_count = 0

    def generate_basic_test_suite(self,max_tokens):

        """
        Generate tests using the AI model based on the constructed prompt.

        This method generates tests by calling the AI model with the constructed prompt.
        It handles both dry run and actual test generation scenarios. In a dry run, it returns canned test responses.
        In the actual run, it calls the AI model with the prompt and processes the response to extract test
        information such as test tags, test code, test name, and test behavior.

        Parameters:
            max_tokens (int, optional): The maximum number of tokens to use for generating tests. Defaults to 4096.
            dry_run (bool, optional): A flag indicating whether to perform a dry run without calling the AI model. Defaults to False.

        Returns:
            dict: A dictionary containing the generated tests with test tags, test code, test name, and test behavior. If an error occurs during test generation, an empty dictionary is returned.

        Raises:
            Exception: If there is an error during test generation, such as a parsing error while processing the AI model response.
        """
        self.logger.info("Starting to Build prompt")
        self.prompt = self.build_prompt()
        self.logger.info(f"Prompt Build Successfully")

        self.logger.info('Calling model to get response with the above prompt')
        response,promt_token_count,response_token_count = (
            self.ai_caller.call_model(prompt=self.prompt,max_tokens=max_tokens)
        )
        
        self.total_input_token_count += promt_token_count
        self.total_output_token_count += response_token_count
        print(self.prompt.get('user'))
        try:
            tests_dict = load_yaml(
                response,
                keys_fix_yaml=["test_tags", "test_code", "test_name", "test_behavior"],
            )
            if tests_dict is None:
                return {}
        except Exception as e:
            self.logger.error(f"Error during test generation: {e}")
            # Record the error as a failed test attempt
            fail_details = {
                "status": "FAIL",
                "reason": f"Parsing error: {e}",
                "exit_code": None,  # No exit code as it's a parsing issue
                "stderr": str(e),
                "stdout": "",  # No output expected from a parsing error
                "test": response,  # Use the response that led to the error
            }
            # self.failed_test_runs.append(fail_details)
            tests_dict = []
        return tests_dict
    
    def build_prompt(self):
        """
        Builds a prompt using the provided information to be used for generating tests.

        This method calls the PromptBuilder class to construct the prompt.
        The prompt includes details such as the source file path.
        Returns:
            str: The generated prompt to be used for test generation.
        """
        # Prompt Builder
        self.logger.info("Initiating Running build_prompt from UnitTestGenerator module")
        self.prompt_builder = PromptBuilder(
            source_file_path=self.source_file_path,
            llm_model=self.llm_model,
        )
        return self.prompt_builder.build_prompt_custom('test_generation_prompt')
    
    
    
    

    def validate_test(self,generated_test: dict,test_class_name: str,test_name: str):
        # Create a new directory for test files
        self.logger.info("Got into validate_test function")
        test_dir = self.test_file_path

        # Create a test file with the number of tests in the filename
        self.logger.info("Creating test_file with the info received")
        test_file_name = f"{test_class_name}.py"
        test_file_path = os.path.join(test_dir, test_file_name)
        
        self.logger.info("Reading the code into test_code variable")
        test_code = generated_test.get('test_code',"").rstrip()
        additional_imports = generated_test.get('new_imports_code',"").strip()
        
        # Check if additional_imports is not empty and is surrounded by double quotes
        if additional_imports and additional_imports.startswith('""') and additional_imports.endswith('""'):
            additional_imports = additional_imports.strip('""')  # Remove the surrounding double quotes
        # If additional_imports only contains double quotes, set it to an empty string
        if additional_imports == '""':
            additional_imports = ""
             

        test_file_path = f'{self.test_file_path}{test_class_name}.java'.replace('\n','')
        with open(test_file_path, 'w', encoding='utf-8') as test_file:
            print(f'writing {test_name.strip()} to file')
            test_file.write(test_code)
            test_file.flush()


        self.logger.info("Passing the test to Runner Class!!!")
        stdout,stderr,exit_code = Runner.run_command(test_class_name,self.maven_file_path)
        self.logger.info("Returned from runner!!!")
        
        if exit_code !=0:
            
            
            self.display_result(test_class_name,exit_code,stderr,stdout)

            result_dict = {
                'status':'FAIL',
                'reason':'Test Failed',
                'exit_code':exit_code,
                'test_name':test_class_name,
                'stderr':stderr,
                'stdout':stdout,
                'test':test_code
            }
            self.delete_test(test_class_name,test_file_path)

        else:
            self.display_result(test_class_name,exit_code,stderr,stdout)
            result_dict = {
                'status':'PASS',
                'reason':'Test PASS',
                'exit_code':exit_code,
                'test_name':test_class_name,
                'stderr':stderr,
                'stdout':stdout,
                'test':test_code
            }
            self.delete_test(test_class_name,test_file_path)
        return result_dict


    def combine_pass_test(self,passed_test: dict):
        
        self.logger.info("Entered combine_pass_test function inside UnitTestGen class!!")
        
        combined_code = "----------\n"
        
        for test in passed_test:
            if len(test) != 0:
                combined_code = combined_code + test.get('test') + '\n----------\n'
        
        
        final_combined_prompt = self.prompt_builder.build_prompt_combine(combined_code)
        
        self.logger.info('Calling model to get response with the above prompt')
        response,promt_token_count,response_token_count = (
            self.ai_caller.call_model(prompt=final_combined_prompt,max_tokens=4096)
        )
        self.total_input_token_count += promt_token_count
        self.total_output_token_count += response_token_count
        
        try:
            tests_dict = load_yaml(
                response,
                keys_fix_yaml=["test_class_name", "test_code"],
            )
            if tests_dict is None:
                return {}
        except Exception as e:
            self.logger.error(f"Error during test generation: {e}")
            # Record the error as a failed test attempt
            fail_details = {
                "status": "FAIL",
                "reason": f"Parsing error: {e}",
                "exit_code": None,  # No exit code as it's a parsing issue
                "stderr": str(e),
                "stdout": "",  # No output expected from a parsing error
                "test": response,  # Use the response that led to the error
            }
            # self.failed_test_runs.append(fail_details)
            tests_dict = []
            
        return tests_dict
    
    def write_final_test(self, final_test_dict: dict) -> str:
        test_class_name = final_test_dict.get('test_class_name')
        test_code = final_test_dict.get('test_code')
        test_file_path = f'{self.test_file_path}{test_class_name}.java'.replace('\n','')

        
        try:
            with open(test_file_path, 'w', encoding='utf-8') as test_file:
                self.logger.info(f'Writing {test_class_name.strip()} to file')
                test_file.write(test_code)
                test_file.flush()
        except IOError as e:
            self.logger.error(f"Failed to write FINAL TEST {test_class_name.strip()} to FILE: {e}")

        return test_class_name
    
    def display_result(self,test_class_name: str,exit_code: int,stderr: str,stdout: str) ->None:
        status = "PASS" if exit_code == 0 else "FAIL"
        temp_dict = {"Test Name": test_class_name,"Status":status}
        result = [temp_dict]
        
        if status == 'PASS':
            print("\nQuick Test Report")
            print(tabulate(result,headers='keys',tablefmt='fancy_grid'))
            print("\n**********STDERR**********")
            print(stderr)
            print("\n**********STDOUT**********")
            print(stdout)
            print()
            
        else:
            print("\nQuick Test Report")
            print(tabulate(result,headers='keys',tablefmt='fancy_grid'))
            print("\n**********STDERR**********")
            print(stderr)
            print("\n**********STDOUT**********")
            print(stdout)
            print()
            
    def delete_test(self,test_name: str,test_file_path:str) -> None:
        
        self.logger.info(f"Trying to delete the PASSED test{test_name}")
        try:
            os.remove(test_file_path)
            self.logger.info(f"{test_name} DELETED FROM {test_file_path}")
        except FileNotFoundError:
            self.logger.info(f"{test_name} Not Found At {test_file_path}")
        except PermissionError:
            self.logger.info(f"Permission denied to delete {test_name} from {test_file_path}")
        except Exception as e:
            self.logger.info(f"Error::: {e}")
        return None


    def display_coverage(self,maven_path):
        jacoco = '\\target\\site\\jacoco\\jacoco.csv'
        full_path = maven_path + jacoco
        if os.path.exists(full_path) and os.path.isfile(full_path):
            df = pd.read_csv(full_path,index_col = [0])
            coverage_result = []

            coverage_result.append(calculate_coverage(df))
            
            print("\nCode Coverage Quick Overview\n")
            print(tabulate(coverage_result,headers='keys',tablefmt='fancy_grid'))
            print(f"\nTo get the full report check out {full_path}\n")
        else:
            print(f"Invalid path: {full_path} or file not found.")
            
def calculate_coverage(row):
    instruction_total = row['INSTRUCTION_MISSED'].values[0] + row['INSTRUCTION_COVERED'].values[0]
    instruction_coverage = (row['INSTRUCTION_COVERED'].values[0]/instruction_total) * 100 if instruction_total else 0
    return {
        'Class':row['CLASS'].values[0],
        'Instruction Coverage (%)': round(instruction_coverage,2)
    }
        
        
    


