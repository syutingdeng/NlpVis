from datasets import load_dataset

def loaddata():
    dataset = load_dataset('imdb',split="test")
    data= []
    label = []
    result= []
    #esult= dataset.filter(lambda example: example['label'] == dataset.features['label'].str2int('equivalent'))[1]
    for i in range(10):
        data_result = "[CLS] "+dataset[i]["text"][:500]
        data.append(data_result)
        data_lable =dataset[i]["label"]
        label.append({"label":data_lable})
    for i in range(13000,13010):
        data_result = "[CLS] "+dataset[i]["text"][:500]
        data.append(data_result)
        data_lable =dataset[i]["label"]
        label.append({"label":data_lable})


    result.append(data)
    result.append(label)
    #print(data[0][0])   
    return result

if __name__ == '__main__':
   print(len(loaddata()[0]))
   


