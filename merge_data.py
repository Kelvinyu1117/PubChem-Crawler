import json

def read_smiles(i):
    """
        read the smiles file
    """
    data = dict()
    with open('smiles/cid_smiles_' + str(i) + '.json', 'r') as file:
        data = json.load(file)
    return data

def save_as_json(data):
    """
        save the dictionary into json file
    """
    with open('smiles/compounds.json', 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    """
        combine all the smiles data into one file 
    """
    compounds = dict()
    cnt = 0
    for i in range(178):
        data = read_smiles(i)
        for item in data:
            if(data[item] != {}):
                compounds[cnt] = data[item]
                cnt += 1
    
    save_as_json(compounds)
    print("Merging data is completed. There are {} data in the file".format(len(compounds)))