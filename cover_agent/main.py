import argparse
import os
from CoverAgent import CoverAgent
from CustomLogger import CustomLogger
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description=f"Cover Agent v")
    parser.add_argument(
        "--source-file-path", required=True, help="Path to the source file."
    )
    parser.add_argument(
        "--destination-file-path", required=True,help="Path to the test file.")
    parser.add_argument(
        "--maven-file-path",required=True,help="Root directory of maven project"
    )
    parser.add_argument(
        "--model",

        default="gpt-4o-mini",
        help="Which LLM model to use. Default: %(default)s.",
    )
    return parser.parse_args()


def main():
    # Initialize logger
    logger = CustomLogger.get_logger(__name__)
    logger.info("Starting CoverAgent application")

    # Parse arguments
    logger.info("Parsing command line arguments")
    args = parse_args()

    # Check if OPENAI_API_KEY is set
    logger.info("Checking if OPENAI_API_KEY environment variable is set")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set")
        return
    logger.info("OPENAI_API_KEY is set")

    # Initialize and run CoverAgent
    logger.info("Initializing CoverAgent with provided arguments")
    agent = CoverAgent(args)
    logger.info("Running CoverAgent")
    agent.run()
    logger.info("CoverAgent run completed successfully")

if __name__ == "__main__":
    main()
