# -*- coding: utf-8 -*-
import os
import requests
from tqdm import tqdm

#conf = 'CVPR2016' # CVPR2015/CVPR2014/CVPR2013/ICCV2013
conf = 'WACV2020' # CVPR2015/CVPR2014/CVPR2013/ICCV2013
#header = 'http://www.cv-foundation.org/openaccess/'
header = 'http://openaccess.thecvf.com/'

def name_check(name):
    name = name.replace('?','')
    name = name.replace(':','')
    name = name.replace('*','')
    name = name.replace('/',' or ')
    return name

def main():
    if not os.path.exists(conf):
        os.mkdir(conf)
    r = requests.get(header+conf+'.py')
    txt = r.text;
    lines = txt.split('\n')
    cnt = 0
    for line in tqdm(lines):
        if line.find('<dt class="ptitle">')>-1:
            pdfname = conf+'/'+name_check(line.split('>')[3].split('<')[0])+'.pdf'
            cnt+=1
        if len(line)>0:
            if line[0]=='[':
                print(str(cnt)+':'+pdfname)
                if not os.path.exists(pdfname):
                    url = header+line.split('"')[1]
                    r = requests.get(url)
                    f = open(pdfname, 'wb')
                    f.write(r.content)
                    f.close()

if __name__ == '__main__':
    main()
    cmd = 'find ./' + str(conf) + ' -name "* *" | rename "s/ /_/g"'
    print(cmd)
    os.system(cmd)
