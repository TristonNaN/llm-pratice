from book.content import ContentType


class LLMModel:

    def make_text_prompt(self, text: str, target_language: str) -> str:
        return f"翻译为{target_language}：{text}"

    def make_table_prompt(self, table: str, target_language: str) -> str:
        return f"翻译为{target_language}，保持间距（空格，分隔符），以表格形式返回：\n{table}"

    def make_prompt(self, content: str, target_language: str) -> str:
        return self.make_text_prompt(content, target_language)

    def make_request(self, prompt):
        raise NotImplementedError("子类必须实现 make_request 方法")