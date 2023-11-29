import argparse
import yaml

class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Translate English PDF book to Chinese.')
        self.parser.add_argument('--config', type=str, default='config.yaml',
                                 help='Configuration file with model and API settings.')
        self.parser.add_argument('--model_type', type=str, required=True, choices=['GLMModel', 'OpenAIModel'],
                                 help='The type of translation model to use. Choose between "GLMModel" and "OpenAIModel".')

    def parse_config(self, config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def parse_arguments(self):
        args, unknown = self.parser.parse_known_args()
        config = self.parse_config(args.config)

        self.parser.add_argument('--glm_model_url', type=str, default=config['GLMModel']['model_url'],
                                 help='The URL of the ChatGLM model URL.')
        self.parser.add_argument('--timeout', type=int, default=config['GLMModel']['timeout'],
                                 help='Timeout for the API request in seconds.')
        self.parser.add_argument('--openai_model', type=str, default=config['OpenAIModel']['model'],
                                 help='The model name of OpenAI Model. Required if model_type is "OpenAIModel".')
        self.parser.add_argument('--input_file_path', type=str, default=config['common']['input_file_path'],
                                 help='The file path of translated book.')
        self.parser.add_argument('--output_file_path', type=str, default=config['common']['output_file_path'],
                                 help='The output file path of translated book.')
        self.parser.add_argument('--output_file_format', type=str, default=config['common']['output_file_format'],
                                 help='The file format of translated book. Now supporting PDF and Markdown')

        args = self.parser.parse_args()
        return args
