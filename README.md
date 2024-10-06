# Cover Agent

Cover Agent is a tool designed to generate unit tests for your code, aiming to achieve high code coverage. It utilizes advanced language models to analyze source files and produce comprehensive test cases.

## Features

- **Unit Test Generation**: Automatically generates unit tests for various programming languages.
- **Customizable Models**: Choose from different language models to suit your needs.
- **Environment Variable Support**: Uses environment variables for sensitive information like API keys.
- **Logging**: Integrated logging for better tracking and debugging.

## Requirements

- Python 3.7 or higher
- Required Python packages (install via `pip`):
  - `argparse`
  - `os`
  - `pandas`
  - `openai`
  - `python-dotenv`
  - `wandb` (optional, for tracking experiments)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cover_agent.git
   cd cover_agent
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Usage

To run the Cover Agent, use the following command:

### Command Line Arguments

- `--source-file-path`: Path to the source file you want to generate tests for.
- `--destination-file-path`: Path where the generated test file will be saved.
- `--maven-file-path`: Root directory of your Maven project.
- `--model`: (Optional) Specify the language model to use. Default is `gpt-4o-mini`.

## Logging

The application uses a custom logger to log important information and errors. Logs are printed to the console and can be redirected to a file if needed.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please reach out to [your_email@example.com].