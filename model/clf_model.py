import torch
from encoder import Encoder

class InterestClassificationModel:
    def __init__(self):
        self.model = torch.nn.Sequential(
            torch.nn.Linear(in_features=768, out_features=128),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=128, out_features=128),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=128, out_features=128),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=128, out_features=2)
        )
        self.model.load_state_dict(torch.load("clf_model.pth", map_location=torch.device('cpu'), weights_only=True))
        self.model.eval()
        self.encoder = Encoder()

    def predict(self, text):
        embedding = self.encoder.encode(text)
        logits = self.model(embedding)
        pred = torch.softmax(logits, dim=1).argmax(dim=1)
        return pred
    
    
    def many_predict(self, texts):
        embeddings = self.encoder.encode(texts)
        logits = self.model(embeddings)
        pred = torch.softmax(logits, dim=1).argmax(dim=1)
        return pred