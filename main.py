import requests
import time
import aiohttp
import asyncio
import random
import json
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

        nsc_nums = list(nsc_nums)  # filter duplicate element
        nsc_nums.sort()
        print('Read the file successfully, there are {} and {} different NSC number in the file.'.format(
            i, len(nsc_nums)))

    return nsc_nums

def write_json(data):
    with open('cid_nsc.json', 'w') as file:
        json.dump(data, file)

def read_json():
    with open('cid_nsc.json', 'r') as file:
        return json.load(file)

def getUrl(nsc_nums):
    return [(item , 'https://pubchem.ncbi.nlm.nih.gov/compound/nsc_' + str(item)) for item in nsc_nums]

def slice_url(urls, size=100):
    return [urls[i:i + size] for i in range(0, len(urls),size)]

def crawler(urls):
    info = dict()
    count = [0, 0]

    async def fetch(url):
        headers = [
            { 'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19'},
            { 'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'},
            { 'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'},
            { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0'},
            { 'User-Agent': 'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0'},
            { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'},
            { 'User-Agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'},
            { 'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'},
            { 'User-Agent': 'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3'}]
        
        async with aiohttp.ClientSession(headers=random.choice(headers)) as session:
            await asyncio.sleep(3)
            async with session.get(url) as res:
                return await res.text()


    async def getCID(nsc, url):
        info["nsc_map_cid"] = list()
        info["duplicate"] = list()
    
        res = await fetch(url)
        compound_html = bs(res, 'html.parser')
        compound_cid = compound_html.find('meta', {'name': 'pubchem_uid_value'})
        if(compound_cid is not None):
            info["nsc_map_cid"].append((nsc, compound_cid["content"]))
        else:
            info["duplicate"].append(nsc)
        
        print("Item {} is finished.".format(count[0]))
        count[0] += 1

    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(getCID(nsc, url)) for nsc, url in urls]
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    return info

def main():
    nsc_nums = read_file()
    urls = getUrl(nsc_nums)
    url_batches = slice_url(urls)
    
    cid_map_nsc = dict()
    write_json(cid_map_nsc)

    for i in range (5):
        print("Batche size: " + str(len(url_batches[i])))
        t1 = time.time()
        new_data = crawler(url_batches[i])
        t2 = time.time() 
        print('Batch {} is Finish! It takes {}s'.format(i,(t2 - t1)))

        cid_map_nsc = read_json()
        cid_map_nsc.update(new_data)
        write_json(cid_map_nsc)

        time.sleep(15)
       


if __name__ == '__main__':
    main()
