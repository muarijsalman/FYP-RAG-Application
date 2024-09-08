import open_clip
from PIL import Image


class EmbeddingModel:
    def __init__(self):
        self.model, _, self.preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
        self.tokenizer = open_clip.get_tokenizer('ViT-B-32')

    def encode_image(self, img: Image):
        image = self.preprocess(img).unsqueeze(0)
        image_features = self.model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)
        return image_features

    def encode_text(self, text):
        text = self.tokenizer(text)
        text_features = self.model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features
