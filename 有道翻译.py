""" 
- URL: http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule
  - url
    - 由于有反爬，一直显示{"errorCode":50}，网上有人提示去掉参数_o，爬虫成功
    - URL: http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule
- Content-Length: 241
  - 长度应该是表单内容的长度
- User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.  4044.92 Safari/537.36 Edg/81.0.416.50    #游览器一些标识 我的是edg，微软
  - 防止被反爬虫，加个伪装身份
- i: hello  
  - 参数
- salt: 15866130639860
  - 时间戳
- sign: 5eaba662ba667122522d389452dcb2ae
  - md5加密后的数据
    - sign: n.md5("fanyideskweb" + e + i + "Nw(nmmbP%A-r6U3EUn]Aj")
    - r = "" + (new Date).getTime()
    - i = r + parseInt(10 * Math.random(), 10);
"""
from urllib import request,parse    #
import random
import time
import json
import hashlib

def salt():
    salts = int(time.time() * 1000) + random.randint(0, 10)
    return salts

def sign(value):
    md5 = hashlib.md5()
    md5.update(bytes(value,encoding='utf-8'))
    sign = md5.hexdigest()
    return sign

def yd_spider(data):
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    signs = "fanyideskweb" + str(data) + str(salt()) + "sr_3(QOHT)L2dx#uuGR@r"    #未经md5加密的
    datas = {   #不管三七二十一，全部装入
        'i': data,       #要翻译的内容
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': str(salt()),  #时间戳，写个函数装一下
        'sign': sign(signs),  #用hashleib写个函数装一下 
        'ts': '1586613063986',
        'bv': '2083a8ac12524fb8e1481a1cf8589e63',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }
    data = parse.urlencode(datas)   #用parse将datas表单数据格式化一下

    headers = {     #为了防止出现各种异常，都装入吧，删除一些不必要的,但是要注意参数长度会变化
        'content-length': len(data),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.50'
    }

    rsq = request.Request(url, data=bytes(data, encoding='utf-8'), headers=headers)
    res = request.urlopen(rsq)

    html = res.read().decode()
    translate_results = json.loads(html)

    # 找到翻译结果
    if 'translateResult' in translate_results:
        translate_results = translate_results['translateResult'][0][0]['tgt']#取到json数据中的"tgt"的value就是我们想要的
        print("\n翻译的结果是：%s" % translate_results)
    else:
        print(translate_results)

if __name__ == "__main__":
    word = input("输入翻译的内容：")
    yd_spider(word)
