import requests, json
from bs4 import BeautifulSoup

api_key = ""
with open('./config/keys.json', 'r') as f:
    api_key = json.load(f)['api_key']

params = "&method=target_code&q="
wordList = []

def checkWords(url):
    global wordList
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    # 단어 존재 유무 확인
    check = soup.find('total')
    if check is None or check.get_text() == '0':
        with open('wordList.txt', 'a', encoding='utf-8') as f:
            for word in wordList:
                f.write(word+'\n')
        print("API로 받아온 단어 존재x. 누적된 " + str(len(wordList)) + "개 단어 저장 완료.")
        wordList = []
        return (-1, "")
    
    # 단어 유형 파악
    wordPos = soup.find('pos')
    wordCat = soup.find('cat')
    wordType = soup.find('type')

    # 추출한 단어
    word = soup.find('word')
    if word is not None:
        word = word.get_text().strip()

    # 단어 유효성 검사
    if len(word) < 2:
        return (-2, "")
    elif wordPos is not None and wordPos.get_text().strip() != "명사":
        return (-3, "")
    elif wordType is not None and wordType.get_text().strip() != "일반어":
        return (-4, "")
    elif wordCat is not None:
        return (-5, "")
    elif word.count('-') > 0 or word.count('^') > 0 or word.count(' ') > 0:
        return (-6, "")
    else:
        return (0, word)

# API 문서의 500000번째 index까지 조회
for i in range(50010, 50010):
    url = "https://opendict.korean.go.kr/api/view?key=" + api_key + params + str(i)
    checkRes, word = checkWords(url)
    if checkRes == 0 and word not in wordList:
        print(word)
        wordList.append(word)

f = open('wordList.txt', 'a')
for word in wordList:
    f.write(word+'\n')
f.close()

print("누적된 나머지 " + str(len(wordList)) + "개 단어 저장 완료.")