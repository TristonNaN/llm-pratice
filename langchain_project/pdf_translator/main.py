from models.translator_chain import TranslatorChain
from translator.pdf_translator import PDFTranslator
from utils.argument_parser import ArgumentParser

if __name__ == "__main__":
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 示例化 LLMChain 类
    translator_chain = TranslatorChain(args.model_name)

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(translator_chain)
    translator.translate_pdf(args.file_path, args.output_file_path, args.output_file_format)

