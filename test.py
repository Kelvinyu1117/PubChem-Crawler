import json

def read_smiles(i):
    """
        read the smiles file
    """
    data = dict()
    with open('smiles/cid_smiles_' + str(i) + '.json', 'r') as file:
        data = json.load(file)
    return data

def read_cid(i):
    """
        read the cid file
    """
    data = dict()
    with open('cid/cid_nsc_' + str(i) + '.json', 'r') as file:
        data = json.load(file)
    return data


def test():
    """
        show the number of data in the cid file and the smiles file
        for checking whether the number of data match or not
    """
    totalData1 = 0
    totalData2 = 0
    diff = 0
    for i in range(178):
        lenData1 = 0
        lenData2 = 0
       
        data1 = read_smiles(i)
        data2 = read_cid(i)

        for item in data1: 
            if(data1[item] != {}):
                lenData1 += 1
                totalData1 += 1
        for item in data2: 
            if(item != 'not_found'):
                lenData2 += 1
                totalData2 += 1

        if(lenData1 != lenData2):
            diff += 1
            print(str(i) + ': ' + str(lenData1), lenData2, '**')
        else:
            print(lenData1, lenData2)
    print('-------------------------')
    print('diff: ' + str(diff))
    print(totalData1, totalData2)



if __name__ == "__main__":
    test()
    