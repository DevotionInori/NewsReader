from django.shortcuts import render
from django.http import HttpResponse
import re
import jieba
import jieba.analyse
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote


def __merge_symmetry(sentences, symmetry=('“', '”')):
    '''合并对称符号，如双引号'''
    effective_ = []
    merged = True
    for index in range(len(sentences)):
        if symmetry[0] in sentences[index] and symmetry[1] not in sentences[index]:
            merged = False
            effective_.append(sentences[index])
        elif symmetry[1] in sentences[index] and not merged:
            merged = True
            effective_[-1] += sentences[index]
        elif symmetry[0] not in sentences[index] and symmetry[1] not in sentences[index] and not merged:
            effective_[-1] += sentences[index]
        else:
            effective_.append(sentences[index])

    return [i.strip() for i in effective_ if len(i.strip()) > 0]


def to_sentences(paragraph):
    """由段落切分成句子"""
    sentences = re.split(r"(？|。|！|\…\…)", paragraph)
    sentences.append("")
    sentences = ["".join(i) for i in zip(sentences[0::2], sentences[1::2])]
    sentences = [i.strip() for i in sentences if len(i.strip()) > 0]

    for j in range(1, len(sentences)):
        if sentences[j][0] == '”':
            sentences[j - 1] = sentences[j - 1] + '”'
            sentences[j] = sentences[j][1:]

    return __merge_symmetry(sentences)

def home(resquest):#定义一个函数，第一个参数必须是request
    return render(resquest, 'index.html')

def takeSecond(elem):
    return elem[1]

def calWeight(wordList):
    p=[]
    wl=[]
    for i in range(0,len(wordList)-1):
        word = []
        wordWithWeight=[]
        for j in range(0,len(wordList[i])-1):
            word.append(wordList[i][j][0])
            wordWithWeight.append([wordList[i][j][0],0])
        p.append(word)
        wl.append(wordWithWeight)

    for i in range(0,len(wordList)-2):
        for j in range(i,len(wordList)-1):
            for word in wordList[i]:
                if word[0] in p[j]:
                    wl[j][p[j].index(word[0])][1]+=word[1]/(j-i+1)
    for i in range(0,len(wl)-1):
        wl[i].sort(key=takeSecond,reverse=True)
    return wl



def reading(request):
    global newsContent
    global conList
    conList=None
    resultList = []
    if request.method == "GET":
        newsContent = request.GET.get("news_content",None)
        wordList = []
        if newsContent!=None:
            conList = to_sentences(newsContent)
            for words in conList:
                keyword = jieba.analyse.textrank(words,topK=20,withWeight=True)
                wordList.append(keyword)
            wordList = calWeight(wordList)
            for j,words in enumerate(wordList):
                searchContent=""
                if(len(words)<=4):
                    for item in words:
                        searchContent +=item[0]
                        searchContent += ' '
                else:
                    for i in range(0,4):
                        searchContent +=words[i][0]
                        searchContent += ' '
                f=quote(searchContent)
                if(len(wordList)!=0):
                    f = urllib.request.urlopen('https://image.baidu.com/search/flip?tn=baiduimage&word='+f).read()
                    key = r'thumbURL":"(.+?)"'
                    key1 = re.compile(key)
                    list = re.findall(key1, str(f))
                    resultList.append([list[0],conList[j]])

                #print(words)
                #print(searchContent)


                #print(f)
                #pattern_pic = '"objURL":"(.*?)",'
                #pic_list = re.findall(pattern_pic, f, re.S)
                #print(pic_list[0])
                #print(soup.find_all("a","imglink"))
            #print(resultList)
            return render(request,'reading.html',
                          {"resultList":enumerate(resultList), "length": len(resultList) - 1})
    return render(request, 'reading.html', {"contentList":conList})