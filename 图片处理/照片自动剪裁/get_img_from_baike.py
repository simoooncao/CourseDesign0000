import requests
from bs4 import BeautifulSoup

def get_img_from_baike(star):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    response = requests.get('https://baike.baidu.com/search/word' , params = {'word' : star} , headers = headers)
    with open('test.html' , 'w' , encoding = 'utf-8') as file:
        file.write(response.text)
    soap = BeautifulSoup(response.text , 'lxml')
    soap1 = soap.select('.layout style')
    if len(soap1) != 0:
        soap = soap1[0].string
        img_url = soap.split('background-image')[1].split('\'')[1]
    else:
        soap1 = soap.select('.summary-pic a img')
        if len(soap1) != 0:
            img_url = soap1[0].attrs['src']
        else:
            img_url = ''
    return img_url

def download(file_name):
    error = open('error.txt' , 'a')
    with open(file_name + '.txt' , 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break

            line = line.replace('\n' , '')
            if line == '':
                continue

            print(line)
            url = get_img_from_baike(line)
            if url == '':
                print('获取url失败！失败条目已记录。')
                error.write('%s\n' % line)
                continue

            print('获取url成功！')
            print(url)
            r = requests.get(url)
            with open('./img_raw/' + line + '.jpg' , 'wb') as f:
                f.write(r.content)
            print('下载成功\n')
    error.close()

download('actor')
download('singer')