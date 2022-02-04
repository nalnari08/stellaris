import os
import os.path
import shutil
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import platform, time
from YmlConvertSupporter import YmlConvertSupporter


def getdict(i):
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


if __name__ == "__main__":
    cwd = os.getcwd() + '/'
    print(cwd)
    skip = False
    ycs = YmlConvertSupporter()
    shutil.rmtree(cwd + 'temp', ignore_errors=True)
    shutil.rmtree(cwd + 'localisation/english', ignore_errors=True)
    if os.path.exists('ko') and os.path.exists('en'):
        print('OK, Now Working, Please wait')
        skip = True
    else:
        print("There is not en and ko folder. terminating...")
        time.sleep(5)
        quit()
    print('working')
    shutil.rmtree(cwd + 'temp', ignore_errors=True)
    os.makedirs(cwd + 'localisation/english', exist_ok=True)
    os.makedirs(cwd + 'temp', exist_ok=True)
    root = cwd + 'en/'
    onlyfiles = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))]
    for i in onlyfiles:
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
