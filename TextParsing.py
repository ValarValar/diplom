import codecs
import requests
import lxml
from pathlib import Path
from lxml import html
from lxml.cssselect import CSSSelector

def contFromHtml(html):
    r = requests.get(html)
    #r = requests.get('http://www.cyberforum.ru/cpp-beginners/thread47422.html')
    with codecs.open('test.html', 'wb') as output_file:
      output_file.write(r.text.encode('utf-8'))

    content = Path('test.html').read_text()
    output_file.close()
    return content

def textInOut(content, contWord, fileVar):
    tree = html.fromstring(content)
    textContent=''
    #print(contWord)

    #for s in tree.xpath('.//div[@id="p379887-content"]'):
    for s in tree.xpath('.//div[contains(@id, "content")]'): #Если передавать переменную, то работает некорректно
        textContent += "".join(['\n'+x.strip() for x in s.itertext()])
    #siteOutText = open('siteOutText','a')
    fileVar.write(textContent)

htmlStr = 'http://forum.mybb.ru/viewtopic.php?id=17487'
topicNum = 4000
string1 = 'http://forum.mybb.ru/viewtopic.php?id='
string2 = '&p='
siteOutText = open('siteOutText','w')
content = contFromHtml(htmlStr)
tree = html.fromstring(content)
#textContent=''
#print(tree.xpath('/html/body//a[contains(@href,"amp")][2]/@href'))
#tmp = tree.xpath('.//div[contains(@class, "pagelink")]')[0]

def pagesCount(inTree):
    treeEl = inTree.xpath('.//div[contains(@class, "pagelink")]')
    treeLen = len(treeEl)
    #print(treeLen)
    if treeLen > 0 :
        #post = treeEl[0].text_content()
        post = (inTree.xpath('.//div[contains(@class, "pagelink")]')[0]).text_content()
        #print(type(post))
        pagesCnt = 0;
        for z in range(1,len(post)):
            tmp = post[len(post) - z]
            #print(type(tmp))
            if tmp.isdigit():
                #print(tmp)
                tmp1 = post[len(post) - z - 1]
                if tmp1.isdigit():
                    #print(tmp)
                    pagesCnt = int(tmp1 + tmp)
                    break
                else: 
                    pagesCnt = int(tmp)
                    break
        return pagesCnt
#print(pagesCount())
#for s in tree.xpath('html/body//a[contains(@href, "http://forum.mybb.ru/viewtopic.php?id=17487&amp;p=7")]/@href'):
   # textContent += "".join(['\n'+x.strip() for x in s.itertext()])
#print(textContent)

#textInOut(content, "content", siteOutText)

for j in range(4000, 17488):
    htmlStrNewForCnt =string1 + str(j)
    content = contFromHtml(htmlStrNewForCnt)
    tree = html.fromstring(content)
    print(tree)
    pagesCnt = pagesCount(tree)
    if pagesCnt is None:
        continue
    for i in range(pagesCnt):
        htmlStrNew = string1 + str(j) + string2 + str(i+1)
        print(htmlStrNew)
        content = contFromHtml(htmlStrNew)
        textInOut(content, 'content', siteOutText) 
siteOutText.close()
#http://forum.mybb.ru/viewtopic.php?id=17487&p=2






