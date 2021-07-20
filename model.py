import dataclasses
from transformers import BertTokenizer, BertForSequenceClassification,BertConfig
import torch
from transformers import pipeline
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import umap
from mpl_toolkits.mplot3d import Axes3D
from prepare_data import loaddata


class TransformersModel:
    
    def __init__(self,model_name):
        self.model_name=model_name
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.data = loaddata() ###load from dataset
        
    
    def setModel(self,layer):
        config = BertConfig(num_hidden_layers=layer,output_hidden_states=True)
        self.model = BertForSequenceClassification(config)
        print("-----------------MODEL--------------------")
        print("Model name"+self.model_name+"\n")
        print(self.model)

    def getUserInputHiddenState(self,UserInput,level):# get uesr input hiddenstate
        self.UserInput = UserInput 
        inputs = self.tokenizer(self.UserInput, return_tensors="pt")
        labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
        outputs = self.model(**inputs, labels=labels)
        self.hidden_states = outputs.hidden_states[level][0]
        self.length = outputs.hidden_states[level][0].shape[0]
        print("Hidden Stat layer"+str(level))
        
        return outputs.hidden_states[level][0]
    
    def getDataSetHiddenState(self,level): # get dataset "cls" hiddenstate
        cls_embedding = []
        for index,item in enumerate(self.data):
            if(index%10==0):
                print("#",str(index))
            inputs = self.tokenizer(item, return_tensors="pt",padding='max_length',max_length=50)
            #labels = torch.tensor([1]).unsqueeze(0)  # Batch size 1
            outputs = self.model(**inputs)

            #print("[CLS]embedding:")     
            #print(outputs.hidden_states[level][0][0])
            cls_embedding.append(outputs.hidden_states[level][0][0])##CLS embedding
        self.cls_embedding = cls_embedding
        self.dataset_length = len(cls_embedding)
        print("cls_embedding length",str(self.dataset_length))
       


    def classify(self):
        classifier = pipeline('sentiment-analysis', model=self.model, tokenizer=self.tokenizer)
        classify = []
        for i in self.data:
             classify.append(classifier(i)[0]) 

        self.sentiment = classify
       
        #return classifier(self.UserInput)
    def UserInputClassify(self):
        classifier = pipeline('sentiment-analysis', model=self.model, tokenizer=self.tokenizer)
        return  classifier("I love you")[0]

        
    def umap(self):
        reducer = umap.UMAP(random_state=42)
        word_embedding = []
        for i in range(self.dataset_length):
            word_embedding.append(self.cls_embedding[i].detach().numpy())
        #print(word_embedding)
        word_embedding = np.array(word_embedding)
        word_embedded_reduce = reducer.fit_transform(word_embedding)

        """for i in range(self.length):    
            word_embedding.append(self.hidden_states[i].detach().numpy())
        print(word_embedding)
        word_embedding = np.array(word_embedding)
        word_embedded_reduce = reducer.fit_transform(word_embedding)"""
        
    
        x=[]
        y=[]
        x_min, x_max =  word_embedded_reduce.min(0), word_embedded_reduce.max(0)
        word_embedded_norm = (word_embedded_reduce - x_min) / (x_max - x_min)
        
        #for i in word_embedded_reduce:
        #    x.append(i[0])
        #    y.append(i[1])

        x0=[]
        y0=[]
        x1=[]
        y1=[]
        
        
        for index,item in enumerate(word_embedded_norm):
            if(self.sentiment[index]['label']=='LABEL_0'):
                x0.append(item[0])
                y0.append(item[1])
            else:
                x1.append(item[0])
                y1.append(item[1])
        print(word_embedded_reduce)
        print("=================")
        print(x0)
        print(y0)
        print(x1)
        print(y1)
        plt.scatter(x0,y0,c="red")
        plt.scatter(x1,y1,c="green")
        plt.show()
        #plt.plot(x,y,'ro')
        #
    




model0 = TransformersModel('bert-base-uncased')
model0.setModel(12)
model0.getDataSetHiddenState(12)
model0.classify()
model0.umap()

print(model0.sentiment)


