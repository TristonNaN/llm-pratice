import argparse
import yaml

class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Translate English PDF book to Chinese.')
        self.parser.add_argument('--config', type=str, default='config.yaml',
                                 help='Configuration file with model and API settings.')

    def parse_config(self, config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config

    def parse_arguments(self):
        args, unknown = self.parser.parse_known_args()
        config = self.parse_config(args.config)

        self.parser.add_argument('--model_name', type=str, default=config['model_name'],
                                 help='The model name of OpenAI Model.')
        self.parser.add_argument('--file_path', type=str, default=config['input_file_path'],
                                 help='The file path of translated book.')
        self.parser.add_argument('--output_file_path', type=str, default=config['output_file_path'],
                                 help='The output file path of translated book.')
        self.parser.add_argument('--output_file_format', type=str, default=config['output_file_format'],
                                 help='The file format of translated book. Now supporting PDF and Markdown')

        args = self.parser.parse_args()
        return args
