import logging
import os

from jinja2 import Environment, StrictUndefined

from settings.config_loader import get_settings

MAX_TESTS_PER_RUN = 4


class PromptBuilder:
    def __init__(
        self,
        source_file_path: str,
        llm_model: str,
        included_files: str = "",
        additional_instructions: str = "",
        failed_test_runs: str = "",
        language: str = "java",
    ):
        """
        The `PromptBuilder` class is responsible for building a formatted prompt string by replacing placeholders with the actual content of files read during initialization. It takes in various paths and settings as parameters and provides a method to generate the prompt.

        Attributes:
            prompt_template (str): The content of the prompt template file.
            source_file (str): The content of the source file.
            test_file (str): The content of the test file.
            code_coverage_report (str): The code coverage report.
            included_files (str): The formatted additional includes section.
            additional_instructions (str): The formatted additional instructions section.
            failed_test_runs (str): The formatted failed test runs section.
            language (str): The programming language of the source and test files.

        Methods:
            __init__(self, prompt_template_path: str, source_file_path: str, test_file_path: str, code_coverage_report: str, included_files: str = "", additional_instructions: str = "", failed_test_runs: str = "")
                Initializes the `PromptBuilder` object with the provided paths and settings.

            _read_file(self, file_path)
                Helper method to read the content of a file.

            build_prompt(self)
                Replaces placeholders with the actual content of files read during initialization and returns the formatted prompt string.
        """
        self.logger = logging.getLogger(__name__)
        self.source_file_name = os.path.basename(source_file_path)
        self.source_file = self._read_file(source_file_path)
        self.language = language
        # add line numbers to each line in 'source_file'. start from 1
        self.source_file_numbered = "\n".join(
            [f"{i + 1} {line}" for i, line in enumerate(self.source_file.split("\n"))]
        )
        

    def _read_file(self, file_path):
        """
        Helper method to read file contents.

        Parameters:
            file_path (str): Path to the file to be read.

        Returns:
            str: The content of the file.
        """
        try:
            with open(file_path, "r") as f:
                return f.read()
        except Exception as e:
            return f"Error reading {file_path}: {e}"

    def build_prompt(self) -> dict:
        self.logger.info("Running build_prompt function inside PromptBuilder Class")
        """
        Replaces placeholders with the actual content of files read during initialization, and returns the formatted prompt.

        Parameters:
            None

        Returns:
            str: The formatted prompt string.
        """
        variables = {
            "source_file_name": self.source_file_name,
            "source_file_numbered": self.source_file_numbered,
            "source_file": self.source_file,
            "language": self.language,
            "max_tests": MAX_TESTS_PER_RUN,
        }
        self.logger.info('Passing all the parameters into the template')
        environment = Environment(undefined=StrictUndefined)
        try:
            system_prompt = environment.from_string(
                get_settings().test_generation_prompt.system
            ).render(variables)
            user_prompt = environment.from_string(
                get_settings().test_generation_prompt.user
            ).render(variables)
            
        except Exception as e:
            logging.error(f"Error rendering prompt: {e}")
            return {"system": "", "user": ""}

        self.logger.info("System prompt and user prompt generated")
        return {"system": system_prompt, "user": user_prompt}


    def build_prompt_custom(self, file) -> dict:
        variables = {
            "source_file_name": self.source_file_name,
            "source_file_numbered": self.source_file_numbered,
            "source_file": self.source_file,
            "language": self.language,
            "max_tests": MAX_TESTS_PER_RUN,
        }
        environment = Environment(undefined=StrictUndefined)
        try:
            system_prompt = environment.from_string(
                get_settings().get(file).system
            ).render(variables)
            user_prompt = environment.from_string(get_settings().get(file).user).render(
                variables
            )
        except Exception as e:
            logging.error(f"Error rendering prompt: {e}")
            return {"system": "", "user": ""}

        return {"system": system_prompt, "user": user_prompt}
    
    def build_prompt_combine(self,combined_code: str) -> dict:
        variables = {
            "seperated_test_files":combined_code
        }
        
        environment = Environment(undefined=StrictUndefined)
        
        try:
            system_prompt = environment.from_string(
                get_settings().combine_prompt.system).render(variables)
            user_prompt = environment.from_string(
                get_settings().combine_prompt.user).render(variables)
        except Exception as e:
            logging.error(f"Error rendereing prompt: {e}")
            return {'system':"",'user':""}
        
        return {"system":system_prompt,"user":user_prompt}
            
        
