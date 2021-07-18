from datasets import load_dataset

def loaddata():
    dataset = load_dataset('glue', 'mrpc', split='train')
    data= []
    #esult= dataset.filter(lambda example: example['label'] == dataset.features['label'].str2int('equivalent'))[1]
    for i in range(len(dataset)):
        data.append(dataset[i]["sentence1"])
    return data

print(loaddata())
   


