import os
import hashlib
import requests
import json

from urlparse import urlparse
from threading import Thread
import httplib, sys
from Queue import Queue

concurrent = 1
# session = requests.Session()

archive = 'https://archive.softwareheritage.org'
content = '/api/1/content/'
# sha1_hash = '5d965a2885eb3b5c7ec317a8084a2b5c944b919d'
hashtype = 'sha1'

# key list
exception = 'exception'
license_url = 'license_url'
facts = 'facts'
filetype_url = 'filetype_url'
encoding = 'encoding'
mimetype = 'mimetype'
tool = 'tool'

def doWork():
    while True:
        url = q.get()
        # status, url = getStatus(url)
        # doSomethingWithResult(status, url)
        session = requests.Session()
        content_data = session.get(url)
        content_dict = content_data.json()
        doSomethingWithResult(content_dict, url)
        q.task_done()

# def getStatus(ourl):
#     try:
#         url = urlparse(ourl)
#         conn = httplib.HTTPSConnection(url.netloc)
#         conn.request("HEAD", url.path)
#         res = conn.getresponse()
#         return res.status, ourl
#     except:
#         return "error", ourl

def doSomethingWithResult(content_dict, url):

    if license_url in content_dict:
        session = requests.Session()
        license_dict = session.get(url + '/license/').json()
        content_dict[facts] = license_dict.get(facts)
    if filetype_url in content_dict:
        session = requests.Session()
        filetype_dict = session.get(url + '/filetype/').json()
        content_dict[encoding] = filetype_dict.get(encoding)
        content_dict[mimetype] = filetype_dict.get(mimetype)
        content_dict[tool] = filetype_dict.get(tool)
    # if language_url in content_dict:

    if not exception in content_dict:
        facts_list = content_dict.get(facts)
        if facts_list:
            license_str = ' AND '.join(' '.join(e.get('licenses')) for e in facts_list)
            print(dirfile + ":" + license_str)
        else:
            print(dirfile)
    else:
        print(dirfile)





q = Queue(concurrent * 2)
for i in range(concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()
try:
    # for url in open('urllist.txt'):
    #     q.put(url.strip())
    # q.join()
    for dirname, dirnames, filenames in os.walk('./codes'):
        for filename in filenames:
            dirfile = os.path.join(dirname, filename)
            if os.path.isfile(dirfile):
                f = open(dirfile, 'rb')
                data = f.read()
                f.close()
                sha1_hash = hashlib.sha1(data).hexdigest()
                url = archive + content + hashtype + ':' + sha1_hash
                q.put(url.strip())
    q.join()
except KeyboardInterrupt:
    sys.exit(1)












#
#
# # session create
# session = requests.Session()
#
# for dirname, dirnames, filenames in os.walk('./codes'):
#     # print path to all subdirectories first.
#     # for subdirname in dirnames:
#     #     print(os.path.join(dirname, subdirname))
#
#     # print path to all filenames.
#     for filename in filenames:
#         # print(os.path.join(dirname, filename))
#         dirfile = os.path.join(dirname, filename)
#         if os.path.isfile(dirfile):
#             f = open(dirfile, 'rb')
#             data = f.read()
#             f.close()
#             sha1_hash = hashlib.sha1(data).hexdigest()
#             content_data = session.get(url + content + hashtype + ':' + sha1_hash)
#             content_dict = content_data.json()
#
#             if license_url in content_dict:
#                 license_dict = session.get(url + content + hashtype + ':' + sha1_hash + '/license/').json()
#                 content_dict[facts] = license_dict.get(facts)
#             if filetype_url in content_dict:
#                 filetype_dict = session.get(url + content + hashtype + ':' + sha1_hash + '/filetype/').json()
#                 content_dict[encoding] = filetype_dict.get(encoding)
#                 content_dict[mimetype] = filetype_dict.get(mimetype)
#                 content_dict[tool] = filetype_dict.get(tool)
#             # if language_url in content_dict:
#
#             if not exception in content_dict:
#                 facts_list = content_dict.get(facts)
#                 license_str = ' AND '.join(' '.join(e.get('licenses')) for e in facts_list)
#                 print(dirfile + ":" + license_str)
#             else:
#                 print(dirfile)
#
#     # Advanced usage:
#     # editing the 'dirnames' list will stop os.walk() from recursing in the there.
#     if '.git' in dirnames:
#         # don't go into any .git directoreis.
#         dirnames.remove('.git')
