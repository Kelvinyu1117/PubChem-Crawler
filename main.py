import requests
import time
from bs4 import BeautifulSoup as bs


def read_file():
    """""
        Read the file and return a list of NSC number
    """""
    nsc_nums = set()
    with open('CANCER60GI50.LST') as file:
        i = 0
        next(file)
        for line in file:
            current_line = line.split(',')
            nsc_nums.add(int(current_line[0].rstrip()))
            i += 1

        nsc_nums = list(nsc_nums) # filter duplicate element
        nsc_nums.sort()
        print('Read the file successfully, there are {} and {} different NSC number in the file.'.format(i, len(nsc_nums)))
    
    return nsc_nums

def getCID(nsc_nums):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    base_url = 'https://pubchem.ncbi.nlm.nih.gov/compound/nsc_'
    
    compound_identifiers = list()

    i = 1

    t1 = time.time()

    for item in nsc_nums: 
        compound_request = requests.get(base_url + str(item), headers = headers)
        compound_html = bs(compound_request.content, 'html.parser')
        compound_cid = compound_html.find('meta', {'name': 'pubchem_uid_value'})["content"]
        compound_identifiers.append((nsc_nums, compound_cid))
        print('Finish crawling item {}'.format(i))
        i += 1

    t2 = time.time()
    print('Get the CIDs successfully, it takes {}s'.format(t2 - t1))


def main():
    nsc_nums = read_file()
    getCID(nsc_nums)







if __name__ == '__main__' :
    main();