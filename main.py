import os
import os.path
import shutil
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import platform, time
from YmlConvertSupporter import YmlConvertSupporter


def getdict(i):
    try:
        if not os.path.exists(i):
            print(i + 'dosen\'t exists')
        f = ''
        try:
            f = (open(i, 'r', encoding='utf-8-sig'))
        except:
            f = (open(i, 'r', encoding='utf-8'))
        dat = f.read().splitlines()
        f.close()
        da_dict = {}
        for x in dat:
            try:
                v = x.split('=', 1)
                da_dict[v[0]] = x
            except:
                print(Exception)
        return da_dict
    except:
        print(i + '변환 중 오류')
        raise Exception

if __name__ == "__main__":
    cwd = os.getcwd() + '/'
    print(cwd)
    skip = False
    ycs = YmlConvertSupporter()
    shutil.rmtree(cwd + 'temp', ignore_errors=True)
    shutil.rmtree(cwd + 'localisation/english', ignore_errors=True)
    if os.path.exists('ko') and os.path.exists('en'):
        print('skiping download')
        skip = True
    if not skip:
        shutil.rmtree(cwd + 'en', ignore_errors=True)
        shutil.rmtree(cwd + 'ko', ignore_errors=True)
        print('downloading')
        resp = urlopen("https://github.com/readingsnail/hoi4/archive/refs/heads/main.zip")
        zipfile = ZipFile(BytesIO(resp.read()))
        print('extracting')
        zipfile.extractall(cwd + 'temp/')
        if not (platform.system() == 'Windows'):
            print('waiting..')
            time.sleep(5)
        shutil.move(cwd + 'temp/hoi4-main/en', cwd)
        shutil.move(cwd + 'temp/hoi4-main/ko', cwd)
    print('working')
    shutil.rmtree(cwd + 'temp', ignore_errors=True)
    os.makedirs(cwd + 'localisation/english', exist_ok=True)
    os.makedirs(cwd + 'temp', exist_ok=True)
    root = cwd + 'en/'
    onlyfiles = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]
    fFiles = []
    for i in onlyfiles:
        if ".properties" in i:
            fFiles.append(i)
    for i in fFiles:
        da = getdict(cwd + 'en/' + i)
        da.update(getdict(cwd + 'ko/' + i))

        output = ''
        for x in da:
            output += da[x] + '\n'
        f = open(cwd + 'temp/' + i, 'w', encoding='utf-8-sig')
        f.write(output)
        f.close()
    ycs.convDirAll()
    shutil.rmtree('temp', ignore_errors=True)
    if not skip:
        shutil.rmtree('en', ignore_errors=True)
        shutil.rmtree('ko', ignore_errors=True)
