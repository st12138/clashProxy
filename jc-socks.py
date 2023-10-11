import threadpool
import random
import argparse
import http.client
import urllib3
import base64
import requests
import json


from urllib.parse import urlparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

TARGET_URI = "/configs"
f = open('a.txt','a')
def  strp(host):
    url = host+TARGET_URI
    #print(url)
    try:
        r = requests.get(url,timeout=2,verify=False)
        if r.status_code == requests.codes.ok:
            data = json.loads(r.text.replace('\n',''))
            #print (data)
            if data["mixed-port"] == 0:
                print(urlparse(host).hostname+':'+str(data["socks-port"]))
                f.write(urlparse(host).hostname+':'+str(data["socks-port"])+'\n')
            else:
                print(urlparse(host).hostname+':'+str(data["mixed-port"]))
                f.write(urlparse(host).hostname+':'+str(data["mixed-port"])+'\n')
    except:
        pass




def multithreading(filename, pools=5):
    works = []
    with open(filename, "r") as f:
        for i in f:
            func_params = [i.rstrip("\n")]
            works.append((func_params, None))
    pool = threadpool.ThreadPool(pools)          #成立线程池
    reqs = threadpool.makeRequests(strp, works)  #修改函数
    [pool.putRequest(req) for req in reqs]
    pool.wait()

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-u",
                        "--url",
                        help="Target URL; Example:http://ip:port")
    parser.add_argument("-f",
                        "--file",
                        help="Url File; Example:url.txt")


    args = parser.parse_args()
    url = args.url
 
    file_path = args.file

    if url != None and file_path ==None:
        pass
    elif url == None and file_path != None:
        multithreading(file_path, 10)  # 默认15线程
    f.close()
if __name__ == "__main__":
    main()
