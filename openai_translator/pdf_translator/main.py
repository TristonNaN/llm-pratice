from translator.pdf_translator import PDFTranslator
from utils.argument_parser import ArgumentParser
from utils.model_loader import ModelLoader

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 示例化 LLMModel 类
    model_loader = ModelLoader()
    model = model_loader.load_model(args)

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(args.input_file_path, args.output_file_path, args.output_file_format)

