from typing import Optional

from common_utils.my_logger import logger
from models.translator_chain import TranslatorChain

from translator.pdf_parser import PDFParser
from translator.pdf_writer import PDFWriter


class PDFTranslator:
    def __init__(self, translator_chain: TranslatorChain):
        self.pdf_parser = PDFParser()
        self.pdf_writer = PDFWriter()
        self.translator_chain = translator_chain

    def translate_pdf(self, input_file_path: str,
                      source_language: str = "English",
                      target_language: str = 'Chinese',
                      output_file_format: str = 'pdf',
                      output_file_path: str = None,
                      pages: Optional[int] = None):

        self.book = self.pdf_parser.parse_pdf(input_file_path, pages)

        for page_idx, page in enumerate(self.book.pages):
            for content_idx, content in enumerate(page.contents):

                # Translate content.original
                translation, status = self.translator_chain.run(content.get_content_str(), source_language, target_language)
                logger.info(translation)

                # Update the content in self.book.pages directly
                self.book.pages[page_idx].contents[content_idx].set_translation(translation, status)

        self.pdf_writer.save_book(self.book, input_file_path, output_file_path, output_file_format)



