
'''
#   pip install requests
#   pip install Pillow
1.  go to https://console.developers.google.com/
2.  search for custome api_key
3.  Create new project to enable custom api_key
4.  Go to credentials tab and create a new API key
5.  Copy API key
6.  On Dashboard Enable the Customsearch API
7.  Go to https://cse.google.com/cse/manage/all
8.  Create new search engine
9.  Enter www.google.com and press save
10. Click on Control Panel and in details field click on Search Engine Id to get cx value
'''


import requests
import json
import os
from PIL import Image
import StringIO
import conf

##----------------------------------------Conf Section----------------------------------------------##
key = conf.key         #Step 4-5
startIndex = [1,11]
cx = conf.cx
##----------------------------------------Conf Section End------------------------------------------##

def download_image(path,searchTerm):
    cnt = 0
    # s = 'Primawatch. Emporio Armani AR0492'.encode('ascii','ignore')
    # print s.replace(' ','_').replace('.','').decode('unicode_escape').encode('ascii','ignore')
    while(cnt < 2):
        searchUrl = "https://www.googleapis.com/customsearch/v1?q=" + \
            searchTerm + "&start=" + str(startIndex[cnt]) + "&key=" + key + "&cx=" + cx +\
            "&searchType=image"
        r = requests.get(searchUrl)
        #response = r.content.decode('utf-8')
        result = json.loads(r.content)

        for item in result['items']:
            #print json.dumps(item,indent = 4)

            url = item['link']
            try:
                image_r = requests.get(url)
            except ConnectionError, e:
                print 'could not download %s' % url
                continue
            # Remove file-system path characters from name.
            title = item['title']
            print '--------------------------------------------------------------------------------------'
            title = title.encode('utf-8','ignore')
            print title
            print '--------------------------------------------------------------------------------------'
            path = '/Users/akashk/Documents/fiverr/googlescrapper/%s' % searchTerm
            if not os.path.exists(path):
                os.makedirs(path)
            file = open(os.path.join(path, '%s.jpg') % title, 'wb')
            try:
                file.write(image_r.content)
            except IOError, e:
                # Throw away some gifs...blegh.
                print 'could not save %s' % url
                continue
            finally:
                file.close()
        cnt = cnt + 1

download_image('/Users/akashk/Documents/fiverr/googlescrapper/', 'AR0492')
