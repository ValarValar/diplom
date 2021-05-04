import sys
import json
from pathlib import Path
import pyconll
import pyconll.tree
import pymorphy2


def process_sentence(sentence, wordArray1):
    flag = False
    elemPunct = [',', '.', '!', '?', '...', "'", '"', "<", ">", "(", ")", ':']
    numAndWordImp = []
    for item in sentence:  # первый обход массива - есть ли повелетильное
        if item.feats.get("Mood") == {"Imp"}:
            lst = []
            num = item.id
            str1 = ""
            for item1 in sentence:
                str1=item1.form
                if item1.head == num and item1.upos == "NOUN":
                    for elem in elemPunct:                          #чистим от лишних символов
                        str1 = str1.replace(elem, "")
                    lst.append(str1.lower())
            str1 = item.form
            for elem in elemPunct:
                str1 = str1.replace(elem, "")
            wordArray1.append((str1.lower(), lst))
            flag = True

conlluFile = 'tes_res2.conllu'
# conlluFile = 'twtexts.txt'
# conlluFile = 'vktexts.txt'
#outDbFile = 'outtest.txt'
# conlluData = pyconll.load_from_file(conlluFile)
#res = []
# print("Файл загрузился")



wordArray = []
for sentence in pyconll.iter_from_file(conlluFile):
    process_sentence(sentence, wordArray)
print(wordArray)



morph = pymorphy2.MorphAnalyzer()

wordDict = {}

for item in wordArray:  # Формирует словарь частоты появлений глаголов
    if len(item[0]) >= 3:
        p = morph.parse(item[0])[0]
        print(p)
        # f.write(item + '\n');
        norm = p.normal_form
        #print(type(wordDict[norm][1]))
        if wordDict.get(norm) is None:
            dict={}
        else:
            dict = wordDict[norm][1]
        for item1 in item[1]:
            if dict.get(item1) is None:
                dict.setdefault(item1, 1)
            else:
                dict[item1] = dict[item1] + 1
        if wordDict.get(norm) is None:
            wordDict.setdefault(norm, (1, dict))
        else:
            wordDict[norm] = (wordDict[norm][0] + 1, dict)
            #print(wordDict[norm])
            #print(wordDict[norm][0])


f = open('words.txt', 'w')
list_d = list(wordDict.items())
#print(list_d)
list_d.sort(key=lambda i: i[1][0], reverse=True)  # Запись в текстовый файл глаголов в нормальной в форме и кол-во появлений
for i in list_d:
    st1=f"Слово: {i[0]} --- Кол-во: {i[1][0]} --- Зависимые слова и их кол-во: {i[1][1]}  \n"
    f.write(st1)
    #f.write(i[0] + ' : ')
    #f.write(str(i[1]) + '\n')
f.close()





