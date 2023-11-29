from typing import Optional

from common_utils.my_logger import logger
from models.llm_model import LLMModel
from translator.pdf_parser import PDFParser
from translator.pdf_writer import PDFWriter


class PDFTranslator:
    def __init__(self, llm_model: LLMModel):
        self.pdf_parser = PDFParser()
        self.pdf_writer = PDFWriter()
        self.llm_model = llm_model

    def translate_pdf(self, input_file_path: str,
                      output_file_path: str = None,
                      output_file_format: str = 'PDF',
                      target_language: str = '中文',
                      pages: Optional[int] = None):

        self.book = self.pdf_parser.parse_pdf(input_file_path, pages)

        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.contents):
                prompt = self.llm_model.make_prompt(content.get_content_str(), target_language)
                logger.info(prompt)
                translation, status = self.llm_model.make_request(prompt)
                logger.info(translation)

                # Update the content in self.book.pages directly
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)

        self.pdf_writer.save_book(self.book, output_file_path, output_file_format)



