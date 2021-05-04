import sys
import json
from pathlib import Path
import pyconll
import pyconll.tree
import pymorphy2


def process_sentence(sentence,wordArray1):
    res = {}
    flag = False
    numAndWordImp=[]
    for item in sentence:   #первый обход массива - есть ли повелетильное
        if item.feats.get("Mood") == {"Imp"}:
            numAndWordImp.append((item.form,item.id))
            flag = True
    if flag:  
        for item in sentence: 
            word = item.form
            pos = item.upos
            mood =""
            feat = item.feats.get("Mood")
            if feat == {"Imp"}:
                mood = "Imp"
                wordArray1.append(item.form)
            parentId = item.head
            rel = item.deprel
            d = {
                'id': item.id,
                'mood': mood,
                'form': item.form,
                'upos': item.upos,
                'parent_id': item.head,
                'deprel': item.deprel
            }
            res[d['id']] = d #Теперь записывает только предложения, где были глаголы в повелительно наклонении
    return res;


conlluFile = 'tes_res2.conllu'
#conlluFile = 'twtexts.txt'
#conlluFile = 'vktexts.txt'
outDbFile = 'outtest.txt'
#conlluData = pyconll.load_from_file(conlluFile)
res = []
#print("Файл загрузился")

wordArray= []
for sentence in pyconll.iter_from_file(conlluFile):
    #print(sentence)
    item = {}
    tree = process_sentence(sentence, wordArray)
    if not (tree == {}):
        ws = []
        for tId, d in sorted(tree.items(), key=lambda p: int(p[0])):
            w = d['form']
            if not w:
                continue
            ws.append(w)
            d['form'] = w.lower()
        item['text_normal'] = ' '.join(ws)
        item['text'] = item['text_normal'].lower()
        item['tree'] = tree
        res.append(item)
jText = json.dumps(res, indent=4, ensure_ascii=False)
#print("1")
Path(outDbFile).write_text(jText)


morph = pymorphy2.MorphAnalyzer()

wordDict = {}
connectedDict = {}
for item in wordArray: #Формирует словарь частоты появлений глаголов
    if len(item) >= 3:
        p = morph.parse(item)[0]
        #f.write(item + '\n');
        norm = p.normal_form
        #print(p.normal_form)
        if wordDict.get(norm) is None:
            wordDict.setdefault(norm, 1)
        else:
            wordDict[norm] = wordDict[norm] + 1


f = open('words.txt', 'w')
list_d = list(wordDict.items())
list_d.sort(key=lambda i: i[1])   #Запись в текстовый файл глаголов в нормальной в форме и кол-во появлений
for i in list_d:
    f.write(i[0] + ' : ')
    f.write(str(i[1]) + '\n')
f.close()



    

