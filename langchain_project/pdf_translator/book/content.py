import re
from enum import Enum, auto

import pandas as pd
from PIL import Image as PILImage


class ContentType(Enum):
    TEXT = auto()
    TABLE = auto()
    IMAGE = auto()


class Content:
    def __init__(self, content_type, original, translation=None):
        self.content_type = content_type
        self.original = original
        self.translation = translation
        self.status = False

    def get_content_str(self):
        raise NotImplementedError("子类必须实现 get_content_str 方法")

    def set_translation(self, translation, status):
        raise NotImplementedError("子类必须实现 set_translation 方法")

    def _set_translation(self, translation, status):
        if not self.check_content_type(self.original):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(translation)}")
        self.translation = translation
        self.status = status

    def check_content_type(self, content):
        if self.content_type == ContentType.TEXT and isinstance(content, str):
            return True
        elif self.content_type == ContentType.TABLE and isinstance(content, pd.DataFrame):
            return True
        elif self.content_type == ContentType.IMAGE and isinstance(content, PILImage.Image):
            return True
        return False


class TextContent(Content):
    def __init__(self, original):
        super().__init__(ContentType.TEXT, original)

    def get_content_str(self):
        if not self.check_content_type(self.original):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(self.original)}")
        return self.original

    def set_translation(self, translation, status):
        self._set_translation(translation, status)


class TableContent(Content):

    def __init__(self, original):
        df = pd.DataFrame(original)
        super().__init__(ContentType.TABLE, df)

    def get_content_str(self):
        if not self.check_content_type(self.original):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(self.original)}")
        return self.original.to_string(header=False, index=False)

    def set_translation(self, translation, status):
        if not isinstance(translation, str):
            raise ValueError(f"Invalid translation type. Expected str, but got {type(translation)}")

        # Convert the string to a list of lists
        table_data = [re.split(r'\s{2,}', row.strip()) for row in translation.strip().split('\n')]
        # Create a DataFrame from the table_data
        translated_df = pd.DataFrame(table_data[1:], columns=table_data[0])

        self._set_translation(translated_df, status)


class ImageContent(Content):
    def __init__(self, original):
        super().__init__(ContentType.IMAGE, original)
