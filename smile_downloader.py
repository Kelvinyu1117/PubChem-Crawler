import pubchempy as pcp
import asyncio
import json


def read_cid(i):
    """
        read the cid file
    """
    data = dict()
    with open('cid/cid_nsc_' + str(i) + '.json', 'r') as file:
        data = json.load(file)

    return data


def save_as_json(data, i):
    """
        save the dictionary into json file
    """
    with open('smiles/cid_smiles_' + str(i) + '.json', 'w') as file:
        json.dump(data, file)


def smile_code_downloader():
    num_of_valid_compound = 0

    def search_smile(cid, nsc):
        """
            get the canonical smiles from pubchem
        """
        c = pcp.Compound.from_cid(cid)
        return c.canonical_smiles

        
    for i in range(178):
        nsc_cid = read_cid(i)
        compounds = dict()
        cnt = 0
        for nsc in nsc_cid:
            data = dict()
            
            if(nsc != 'not_found'):
                data['nsc'] = nsc
                data['cid'] = nsc_cid[nsc]
                data['canonical_smiles'] = search_smile(nsc_cid[nsc], nsc)
                print("Item {} is completed".format(cnt))
                compounds[cnt] = data
                cnt += 1
                num_of_valid_compound += 1
        # save the file after each iteration
        save_as_json(compounds, i)
        print("Number of valid compounds in cid_nsc_{}: {}".format(i, cnt))
        print("Crawling the file cid_nsc_{} is completed".format(i))


    print("Total number of valid compounds: " + str(num_of_valid_compound))



if __name__ == "__main__":
    smile_code_downloader()
    
