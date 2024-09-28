import torch
from transformers import AutoTokenizer, AutoModel


class Encoder:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained("intfloat/multilingual-e5-large-instruct")
        self.encoder = AutoModel.from_pretrained("intfloat/multilingual-e5-large-instruct").to(self.device)

    def encode(self, sentences):
        encoded_input = self.tokenizer(sentences, padding=True, truncation=True, max_length=512, return_tensors='pt')
        with torch.no_grad():
            model_output = self.encoder(**encoded_input.to(self.device))
            embeddings = model_output.pooler_output
            embeddings = torch.nn.functional.normalize(embeddings)
        return embeddings

class InterestClassificationModel:
    def __init__(self):
        print("Cuda is:" + str(torch.cuda.is_available()))
        print(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.__model = torch.nn.Sequential(
            torch.nn.Linear(in_features=1024, out_features=1024),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=1024, out_features=1024),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=1024, out_features=1024),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=1024, out_features=1024),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=1024, out_features=1)
            ).to(self.__device)
        self.__model.load_state_dict(torch.load("clf_interest_model.pth", map_location=self.__device, weights_only=True))
        self.__model.eval()
        self.__encoder = Encoder()

    def predict(self, text):
        embeddings = self.__encoder.encode(text)
        logits = self.__model(embeddings.to(self.__device)).squeeze() 
        pred = torch.sigmoid(logits).to('cpu').tolist()
        pred = [round(x,4) for x in pred]
        return pred

class HumorClassificationModel:
    def __init__(self):
        print("Cuda is:" + str(torch.cuda.is_available()))
        print(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.__model = torch.nn.Sequential(
            torch.nn.Linear(in_features=1024, out_features=1024),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=1024, out_features=1024),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=1024, out_features=1024),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=1024, out_features=1024),
            torch.nn.ReLU(),
            torch.nn.Linear(in_features=1024, out_features=1)
            ).to(self.__device)
        self.__model.load_state_dict(torch.load("clf_humor_model.pth", map_location=self.__device, weights_only=True))
        self.__model.eval()
        self.__encoder = Encoder()

    def predict(self, text):
        embeddings = self.__encoder.encode(text)
        logits = self.__model(embeddings.to(self.__device)).squeeze() 
        pred = torch.sigmoid(logits).to('cpu').tolist()
        pred = [round(x,4) for x in pred]
        return pred