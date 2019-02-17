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

def graph_downloader():
    cnt = [0]

    def img_downloader(cid, nsc):
        """
            download the png image from pubchem, the naming of the image: nsc_number.png
        """
        if(nsc != 'not_found'):
            pcp.download('PNG', 'graph/' + nsc + '.png', cid, overwrite=True)
            print("Item " + str(cnt[0]) + " is completed")
            cnt[0] += 1

    for i in range(178):
        cnt = [0]
        nsc_cid = read_cid(i)
        for nsc in nsc_cid:
            img_downloader(nsc_cid[nsc], nsc)
        print("Crawling the file cid_nsc_{} is completed".format(i))


if __name__ == "__main__":
    graph_downloader()
