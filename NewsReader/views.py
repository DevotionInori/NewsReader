from django.shortcuts import render
from django.http import HttpResponse
import re
import jieba
import jieba.analyse
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote

def home(resquest):#定义一个函数，第一个参数必须是request
    return render(resquest, 'index.html')

def reading(request):
    global newsContent
    global conList
    conList=None
    resultList = []
    if request.method == "GET":
        newsContent = request.GET.get("news_content",None)
        if newsContent!=None:
            conList = re.split(r'。', newsContent) #nltk hanlp
            conList.pop()
            for words in conList:
                keyword = jieba.analyse.textrank(words,topK=20)
                searchContent=""
                if(len(keyword)<4):
                    for item in keyword:
                        searchContent +=item
                        searchContent += ' '
                else:
                    for i in range(0,4):
                        searchContent +=keyword[i]
                        searchContent += ' '
                f=quote(searchContent)
                if(len(keyword)!=0):
                    f = urllib.request.urlopen('https://image.baidu.com/search/flip?tn=baiduimage&word='+f).read()
                    key = r'thumbURL":"(.+?)"'
                    key1 = re.compile(key)
                    list = re.findall(key1, str(f))
                    resultList.append([list[0],words])

                #print(words)
                #print(searchContent)


                #print(f)
                #pattern_pic = '"objURL":"(.*?)",'
                #pic_list = re.findall(pattern_pic, f, re.S)
                #print(pic_list[0])
                #print(soup.find_all("a","imglink"))
            print(resultList)
            return render(request,'reading.html',
                          {"resultList":enumerate(resultList), "length": len(resultList) - 1})
    return render(request, 'reading.html', {"contentList":conList})