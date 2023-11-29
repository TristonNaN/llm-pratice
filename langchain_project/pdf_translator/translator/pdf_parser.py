from typing import Optional

import pdfplumber

from book.book import Book
from book.content import Content, ContentType, TextContent, TableContent
from book.page import Page
from common_utils.my_logger import logger


class PDFParser:
    def __init__(self):
        pass

    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None):

        book = Book()

        with pdfplumber.open(pdf_file_path) as pdf:
            if pages is not None and pages > len(pdf.pages):
                raise Exception(f"Page out of range: Book has {len(pdf.pages)} pages, but {pages} pages were requested.")

            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]

            for pdf_page in pages_to_parse:
                page = Page()

                # Store the original text content
                raw_text = pdf_page.extract_text()
                raw_tables = pdf_page.extract_tables()
                # raw_images =

                # Remove each cell's content from the original text
                for table in raw_tables:
                    for row in table:
                        for cell in row:
                            raw_text = raw_text.replace(cell, "", 1)

                # Handling text
                if raw_text:
                    # Remove empty lines and leading/trailing whitespaces
                    raw_text_lines = raw_text.splitlines()
                    cleaned_raw_text_lines = [line.strip() for line in raw_text_lines if line.strip()]
                    cleaned_raw_text = "\n".join(cleaned_raw_text_lines)

                    text_content = TextContent(original=cleaned_raw_text)
                    page.add_content(text_content)
                    logger.info(f"[raw_text]\n {cleaned_raw_text}")

                if raw_tables:
                    for raw_table in raw_tables:
                        image_content = TableContent(original=raw_table)
                        page.add_content(image_content)
                        logger.info(f"[table]\n{raw_table}")

                # if raw_images:
                #     image_contents = ImageContent(original=raw_images)
                #     page.add_content(image_contents)
                #     logger.info(f"[image]\n{raw_images}")

                book.add_page(page)

            return book