import pubchempy as pcp
import json

def read_cid:
    data = dict()
    with open('cid/cid_nsc_0.json', r) as file:
        data = json.load(file)
    return data

def search_compound():
    pass
if __name__ == "__main__":
    