import os
import requests
from tqdm import tqdm
import argparse


def arg():
    parser = argparse.ArgumentParser(description="PDF Downloader for CVF")
    parser.add_argument('--conf', '-c',
        type=str,
        default='WACV2020',
        help='The target conference name.')
    return parser.parse_args()


def name_check(name):
    name = name.replace('?','')
    name = name.replace(':','')
    name = name.replace('*','')
    name = name.replace('/',' or ')
    return name


def main():
    args = arg()
    header = 'http://openaccess.thecvf.com/'

    if not os.path.exists(args.conf):
        os.mkdir(args.conf)

    r = requests.get(header+args.conf+'.py')
    txt = r.text;
    lines = txt.split('\n')

    cnt = 0
    for line in tqdm(lines):
        if line.find('<dt class="ptitle">')>-1:
            pdfname = args.conf+'/'+name_check(line.split('>')[3].split('<')[0])+'.pdf'
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
    cmd = 'find ./' + str(args.conf) + ' -name "* *" | rename "s/ /_/g"'
    print(cmd)
    os.system(cmd)
