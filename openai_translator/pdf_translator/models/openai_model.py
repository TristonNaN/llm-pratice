import json
import time

import openai
import requests

from common_utils.my_logger import logger
from models.llm_model import LLMModel


class OpenAIModel(LLMModel):

    def __init__(self, model: str):
        self.model = model

    def make_request(self, prompt, attempts=3):

        for i in range(1, attempts + 1):
            try:
                if self.model == "gpt-3.5-turbo":
                    response = openai.ChatCompletion.create(
                        model=self.model,
                        messages=[
                            {"role": "user", "content": prompt}
                        ]
                    )
                    translation = response.choices[0]['message']['content'].strip()
                else:
                    response = openai.Completion.create(
                        model=self.model,
                        prompt=prompt,
                        max_tokens=150,
                        temperature=0
                    )
                    translation = response.choices[0].text.strip()
                return translation, True

            except openai.error.RateLimitError:
                if i <= 3:
                    logger.warning(f"已达到 API 请求的速率限制, 将等待 60s 后重试第{i + 1}次.")
                    time.sleep(60)
                else:
                    raise Exception(f"已达到 API 请求的速率限制, 超过最大重试次数{attempts}.")
            except requests.exceptions.Timeout as e:
                raise Exception(f"请求超时：{e}")
            except requests.exceptions.RequestException as e:
                raise Exception(f"请求异常：{e}")
            except json.JSONDecodeError as e:
                raise Exception(f"响应是无效的 JSON 格式: {e}")
            except Exception as e:
                raise Exception(f"未知错误：{e}")

        return "", False
