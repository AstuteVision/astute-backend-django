import os

from .base import ReId
import torchreid
from django.conf import settings
import torch
import numpy as np
from PIL import Image
from torchvision import transforms


def preprocess_frame(frame, need=False):
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((256, 128), antialias=None),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    preprocessed_frame = preprocess(frame)
    return preprocessed_frame.unsqueeze(0)


class OsNetReid(ReId):
    def __init__(self, ideal_frames: list[tuple[int, str]],
                 weights_path: str = settings.REID_WEIGHTS_PATH,
                 model_name: str = settings.REID_MODEL_NAME,
                 num_classes: int = settings.REID_NUM_CLASSES):
        model = torchreid.models.build_model(
            name=model_name,  # Replace with your model architecture
            num_classes=num_classes,  # Replace with the number of classes in your dataset
        )
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(device)
        torchreid.utils.load_pretrained_weights(model, weights_path)
        model.eval()
        self.model = model
        self.ideal_embeddings = self.get_ideal_embeddings(ideal_frames)

    def predict(self, cropped_image):
        cropped_image = preprocess_frame(cropped_image)
        with torch.no_grad():
            cur_embedding = self.model(cropped_image)
        return self.get_best_match(cur_embedding)

    def get_best_match(self, cur_embedding):
        real_id = -1  # TODO: change to None
        for id, embeddings in self.ideal_embeddings.items():
            for embedding in embeddings:
                if torch.cosine_similarity(cur_embedding, embedding) > 0.7:
                    real_id = id
        return real_id

    def get_ideal_embeddings(self, paths):
        embeddings = {}
        for id, path in paths:
            img = Image.open(path)
            data = np.array(img)
            pre_frame = preprocess_frame(data)
            with torch.no_grad():
                cur_embedding = self.model(pre_frame)
                if id in embeddings:
                    embeddings[id].append(cur_embedding)
                else:
                    embeddings[id] = [cur_embedding]
        return embeddings


frames_for_vector_search = []
ideal_frames_directory = settings.IDEAL_FRAMES_DIRECTORY
for person_id in os.listdir(ideal_frames_directory):
    for person_image in os.listdir(os.path.join(ideal_frames_directory, person_id)):
        frames_for_vector_search.append((int(person_id), os.path.join(ideal_frames_directory, person_id, person_image)))
reid = OsNetReid(frames_for_vector_search)
