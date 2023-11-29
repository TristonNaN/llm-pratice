from models.openai_model import OpenAIModel
from models.glm_model import GLMModel


class BaseModelLoader:
    def __init__(self):
        self.model_loaders = {
            'GLMModel': self.load_glm_model,
            'OpenAIModel': self.load_openai_model
        }

    def load_glm_model(self, args):
        if not args.glm_model_url:
            raise ValueError("GLM model requires 'glm_model_url' argument.")
        model = GLMModel(args.glm_model_url, args.timeout)
        return model

    def load_openai_model(self, args):
        if not args.openai_model:
            raise ValueError("OpenAI model requires 'openai_model' and 'openai_api_key' arguments.")
        model = OpenAIModel(args.openai_model)
        return model


class ModelLoader(BaseModelLoader):
    def load_model(self, args):
        if args.model_type not in self.model_loaders:
            raise ValueError(f"Invalid model_type. Supported types are {list(self.model_loaders.keys())}.")
        model = self.model_loaders[args.model_type](args)
        return model
