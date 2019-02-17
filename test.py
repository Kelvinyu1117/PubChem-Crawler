import json

def read_cid1(i):
    data = dict()
    with open('smiles/cid_smiles_' + str(i) + '.json', 'r') as file:
        data = json.load(file)
    return data

def read_cid2(i):
    data = dict()
    with open('cid/cid_nsc_' + str(i) + '.json', 'r') as file:
        data = json.load(file)
    return data


def test():
    totalData1 = 0
    totalData2 = 0
    diff = 0
    for i in range(178):
        lenData1 = 0
        lenData2 = 0
       
        data1 = read_cid1(i)
        data2 = read_cid2(i)
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
    