import requests
import time
import aiohttp
import asyncio
import random
import json
import pubchempy as pcp
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
        print('Read the file successfully, there are {} lines and {} different NSC numbers in the file.'.format(
            i, len(nsc_nums)))

    return nsc_nums


def write_json(data, i):
    """
        write the nsc_map_cid dictionary to the file
    """
    with open('cid/cid_nsc_' + str(i) + '.json', 'w') as file:
        json.dump(data, file)

def getUrl(nsc_nums):
    return [(item, 'https://pubchem.ncbi.nlm.nih.gov/compound/nsc' + str(item)) for item in nsc_nums]

def slice_url(urls, size=300):
    return [urls[i:i + size] for i in range(0, len(urls), size)]


def cid_crawler(urls):
    cid = dict()
    count = [0]
    cid["not_found"] = list()

    async def fetch(url):
        """
            return the html of the url
        """
        sleep_rand = random.randint(2,12) # generate a random number for thread sleep
        
        headers = [ {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11 Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'},
                    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'},
                    {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},
                    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4'}]
        
        header = random.choice(headers) # randomly select the user agent
        connector = aiohttp.TCPConnector(limit=50, limit_per_host=50)
        async with asyncio.Semaphore(5): 
            async with aiohttp.ClientSession(headers=header, connector=connector) as session:
                await  asyncio.sleep(sleep_rand)
                async with session.get(url, headers=header) as res:
                    return await res.text()


    async def getCID(nsc, url):
        
        res = await fetch(url)
        compound_html = bs(res, 'html.parser')
        compound_cid = compound_html.find('meta', {'name': 'pubchem_uid_value'})
        if(compound_cid is not None):
            cid[nsc] = compound_cid["content"]
        else:
            cid["not_found"].append(nsc)
            
        print("Item {} is finished.".format(count[0]))
        count[0] += 1

    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(getCID(nsc, url)) for nsc, url in urls] # create a list of tasks
    tasks = asyncio.gather(*tasks)
    loop.run_until_complete(tasks)

    return cid


def nsc_2_cid():
    nsc_nums = read_file()
    urls = getUrl(nsc_nums)
    url_batches = slice_url(urls)
    
    print("Number of Batches: " + str(len(url_batches)))

    for i in range (0, len(url_batches)):
        print("Batche size: " + str(len(url_batches[i])))
        t1 = time.time()
        new_data = cid_crawler(url_batches[i])
        t2 = time.time() 
        print('Batch {} is Finished! It takes {}s'.format(i,(t2 - t1)))
        write_json(new_data, i)
        """ if(i % 8 == 0):
            time.sleep(60)
        else:
            time.sleep(15) """

    



if __name__ == '__main__':
    nsc_2_cid()
