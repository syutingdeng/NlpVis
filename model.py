from transformers import BertTokenizer, BertForSequenceClassification
import torch
import transformers
import numpy as np
from sklearn.manifold import TSNE


class TransformersModel:
   
    def __init__(self,model_name):
        self.model_name=model_name
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name,output_hidden_states=True)

    def getModelHiddenState(self,level):
        inputs = self.tokenizer("Hello, my dog is cute", return_tensors="pt")
        labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
        outputs = self.model(**inputs, labels=labels)
        #return outputs[2][level].detach().numpy()
        return outputs.hidden_states[level][0]
    

    


model0 = TransformersModel('bert-base-uncased')
print(model0.getModelHiddenState(0).shape)