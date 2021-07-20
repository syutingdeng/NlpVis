from datasets import load_dataset

def loaddata():
    dataset = load_dataset('glue', 'mrpc', split='train')
    data= []
    #esult= dataset.filter(lambda example: example['label'] == dataset.features['label'].str2int('equivalent'))[1]
    for i in range(50):
        result = "[CLS] "+dataset[i]["sentence1"]
        data.append(result)
    print(data[0][0])   
    return data

if __name__ == '__main__':
   print(loaddata())
   


