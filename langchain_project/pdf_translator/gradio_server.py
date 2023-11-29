import gradio

from common_utils.my_logger import logger
from models.translator_chain import TranslatorChain
from translator.pdf_translator import PDFTranslator
from utils.argument_parser import ArgumentParser


def translation(input_file, source_language, target_language):
    logger.debug(f"[翻译任务]\n源文件: {input_file.name}\n源语言: {source_language}\n目标语言: {target_language}")

    output_file_path = Translator.translate_pdf(
        input_file.name, source_language=source_language, target_language=target_language)

    return output_file_path


def launch_gradio():
    iface = gradio.Interface(
        fn=translation,
        title="OpenAI-Translator v2.0(PDF 电子书翻译工具)",
        inputs=[
            gradio.File(label="上传PDF文件"),
            gradio.Textbox(label="源语言（默认：英文）", placeholder="English", value="English"),
            gradio.Textbox(label="目标语言（默认：中文）", placeholder="Chinese", value="Chinese")
        ],
        outputs=[
            gradio.File(label="下载翻译文件")
        ],
        allow_flagging="never"
    )

    iface.launch(share=False)


def initialize_translator():
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()

    # 示例化 LLMChain 类
    translator_chain = TranslatorChain(args.model_name)

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    global Translator
    Translator = PDFTranslator(translator_chain)


if __name__ == "__main__":
    # 初始化 translator
    initialize_translator()
    # 启动 Gradio 服务
    launch_gradio()
