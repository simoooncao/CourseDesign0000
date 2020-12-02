import requests
import time
import random
import urllib
import hashlib
import base64
from PIL import Image
from io import BytesIO

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class TencentAICommunication(object):
    def __init__(self):
        self.app_id = '2160113365'
        self.app_key = 'Pz4PzcIHrEdS6Q5k'

    def get_face_info(self , img_bytes):
        request_url = 'https://api.ai.qq.com/fcgi-bin/face/face_detectface'
        img = self.img_bytes_to_base64(img_bytes)
        data = {'image' : img , 'mode' : '0'}
        data = self._gen(data)
        respone = requests.post(request_url , data)
        result_dict = respone.json()
        print(result_dict)
        result = ['检测成功']
        if result_dict['ret'] == 16404:
            return [16404]
        if result_dict['ret'] != 0:
            return ['检测失败']
        each = result_dict['data']['face_list'][0]
        # print(each)
        x = each['x']
        y = each['y']
        w = each['width']
        h = each['height']
        result.append((x , y , w , h))
        return result

    def img_bytes_to_base64(self , img_bytes):
        im_base64 = base64.b64encode(img_bytes)
        return im_base64.decode('utf-8')

    def img_base64_to_bytes(self , b64img):
        im_bytes = base64.b64decode(b64img)
        return im_bytes

    def _gen(self, dict , charset = 'utf-8'):
        chset = charset
        charset = [chr(x) for x in range(0, 127) if 48 <= x <= 57 or 65 <= x <= 90 or 97 <= x <= 122]
        length = random.randint(16, 32)
        nonce_str = ''.join([random.choice(charset) for x in range(length)])
        time_stamp = str(int(time.time()))


        data = {'app_id': self.app_id, 'nonce_str': nonce_str, 'time_stamp': time_stamp}
        data = self._merge(data, dict)

        # 要求编码为utf-8
        urlkey = []
        for each in data:
            key = data[each]
            key = urllib.parse.quote(key.encode(chset), safe='')
            urlkey.append(each + '=' + key)
        urlkey = '&'.join(urlkey) + '&app_key=' + self.app_key
        urlkey = urlkey.replace('%20' , '+')
        # print(urlkey)

        m = hashlib.md5()
        m.update(urlkey.encode(chset))
        sign = m.hexdigest().upper()
        data['sign'] = sign

        return data

    def _merge(self , dict1 , dict2):
        res = {}
        len1 , len2 = len(dict1) , len(dict2)
        i , j = 0 , 0
        key1 , key2 = list(dict1.keys()) , list(dict2.keys())
        while i < len1 and j < len2:
            if key1[i] < key2[j]:
                res[key1[i]] = dict1[key1[i]]
                i = i + 1
            else:
                res[key2[j]] = dict2[key2[j]]
                j = j + 1
        while i < len1:
            res[key1[i]] = dict1[key1[i]]
            i = i + 1
        while j < len2:
            res[key2[j]] = dict2[key2[j]]
            j = j + 1
        return res


@singleton
class BaiduAICommunication:
    def __init__(self):
        self.client_id = 'rayVULaalKzuqvs1LRHGvvTr'
        self.client_secret = 'QUld11gV22wKfK9rKqVLDnVpVHSuIePf'
        self.request_url = 	'https://aip.baidubce.com/rest/2.0/image-process/v1/image_quality_enhance'

    def gen(self):
        url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (self.client_id , self.client_secret)
        res = requests.post(url)
        data = res.json()
        if 'error' in data:
            return (0 , data['error_description'])
        else:
            return (1 , data['access_token'])

    def magnification(self, img_base64):
        a , b = self.gen()
        if a == 0:
            return (a , b)
        else:
            access_token = b

        # data为dict时默认以表单形式提交
        data = {}
        data['image'] = img_base64 #urllib.parse.quote(img_base64.encode('utf-8') , safe = '')
        url = self.request_url + '?access_token=' + access_token
        response = requests.post(url, data)
        result_dict = response.json()
        print(result_dict)

        if 'image' in result_dict:
            return result_dict['image']
        elif result_dict['error_code'] == 216201:
            return -2
        else:
            return -1


tencent = TencentAICommunication()
baidu = BaiduAICommunication()


def base64_to_pillow(img_base64):
    binary_data = BytesIO(base64.b64decode(img_base64))
    im = Image.open(binary_data)
    return im

def pillow_to_base64(img_pillow):
    output_buffer = BytesIO()
    if img_pillow.mode == 'RGB':
        img_pillow.save(output_buffer, format='jpeg')
    else:
        img_pillow.save(output_buffer, format='png')
    byte_data = output_buffer.getvalue()
    return base64.b64encode(byte_data).decode('utf-8')


def resize_image(name):
    print(name)

    try:
        with open('./img_raw/' + name + '.jpg', 'rb') as tf:
            img_bytes = tf.read()
    except:
        print('原始图片不存在\n')
        return

    while True:
        info = tencent.get_face_info(img_bytes)
        if info[0] == '检测成功' or info[0] == 16404:
            break
        time.sleep(1.5)

    if info[0] == 16404:
        err = open('error_resize.txt', 'a')
        err.write('%s\n' % name)
        err.close()
        return
    x, y, w, h = info[1]
    im_pillow = Image.open(BytesIO(img_bytes))
    im_w, im_h = im_pillow.size

    new_x, new_y = x, y
    if y < h:
        top = y
        new_y = 0
    else:
        top = h
        new_y = y - h

    if y + h + 2 * h <= im_h:
        bottom = 2 * h
    else:
        bottom = im_h - y - h

    new_h = top + h + bottom
    side = (new_h - w) / 2
    if im_w < new_h:
        new_h = im_w
        new_x = 0
    else:
        if x <= side:
            new_x = 0
        elif im_w - x - w <= side:
            new_x = x - side - (side - (im_w - x - w))
        else:
            new_x = x - side
    new_w = new_h
    print('自适应调整后关键点：(%d , %d , %d , %d)' % (new_x, new_y, new_w, new_h))

    new_im = im_pillow.crop((new_x, new_y, new_x + new_w, new_y + new_h))
    mode = new_im.mode

    while True:
        res = baidu.magnification(pillow_to_base64(new_im))
        if res != -1:
            break
        time.sleep(1.5)
    if res != -2:
        new_im = base64_to_pillow(res)
    print(new_im.mode)

    new_im = new_im.resize((600, 600), Image.ANTIALIAS)
    if mode == 'RGB':
        new_im.save('./img/' + name + '.jpg', format='jpeg')
    else:
        new_im.save('./img/' + name + '.jpg', format='png')
    print('图片处理完毕\n')

def work(file_name):
    with open(file_name + '.txt' , 'r') as f:
        for line in f:
            name = line.strip()
            if not name:
                continue
            resize_image(name)

work('actor')
work('singer')



