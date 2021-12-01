from datasets import load_dataset
from tagging import pos_tagging

def loaddata():#data,groundtruth,part-of-speech
    dataset = load_dataset('imdb',split="test")
    data= []
    label = []
    result= []
    pos = []
    #esult= dataset.filter(lambda example: example['label'] == dataset.features['label'].str2int('equivalent'))[1]
    for i in range(2):
        data_result = dataset[i]["text"][:500]
        data.append(data_result)
        data_lable =dataset[i]["label"]
        label.append({"label":data_lable})
        pos.append(pos_tagging(data_result))
        
        
    for i in range(13000,13002):
        data_result =dataset[i]["text"][:500]
        data.append(data_result)
        data_lable =dataset[i]["label"]
        label.append({"label":data_lable})
        pos.append(pos_tagging(data_result))
        


    result.append(data)
    result.append(label)
    result.append(pos)
    #print(data[0][0])   
    return result

if __name__ == '__main__':
   print(loaddata())
   


