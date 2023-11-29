import json
import requests

from models.llm_model import LLMModel


class GLMModel(LLMModel):

    def __init__(self, model_url: str, timeout: int):
        self.model_url = model_url
        self.timeout = timeout

    def make_request(self, prompt, attempts=3):

        for i in range(1, attempts + 1):
            try:
                payload = {
                    "prompt": prompt,
                    "history": []
                }
                response = requests.post(self.model_url, json=payload, timeout=self.timeout)
                response.raise_for_status()
                response_dict = response.json()
                translation = response_dict["response"]
                return translation, True
            except requests.exceptions.Timeout as e:
                raise Exception(f"请求超时：{e}")
            except requests.exceptions.RequestException as e:
                raise Exception(f"请求异常：{e}")
            except json.JSONDecodeError as e:
                raise Exception(f"响应是无效的 JSON 格式: {e}")
            except Exception as e:
                raise Exception(f"未知错误：{e}")
        return "", False
