import requests
from bs4 import BeautifulSoup


def search(query):
    l=[]
    i=[]

    phrasel='si'
    phrasei='si'
    query = "https://www.google.com/search?q=" + query

    #"BNeawe s3v9rd AP7Wnd"
    #"BNeawe iBp4i AP7Wnd"
    r = requests.get(query)
    html_doc = r.text
    #print(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser')


    for s in soup.find_all('div',class_="BNeawe iBp4i AP7Wnd"):
        l.append(s.text)
        #print(s.text)
    for s in soup.find_all('div',class_="BNeawe s3v9rd AP7Wnd"):
        i.append(s.text)
        #print(s.text)

    #print(i[2])
    try:
        x = [char for char in i[0]]
        y = [char for char in i[1]]
        if (len(x) < len(y)):
            phrasei = i[0]
        else:
            phrasei = i[1]
    except:
        g=False

    try:
        x = [char for char in l[0]]
        y = [char for char in l[1]]
        if (len(x)<len(y)):
            phrasel=l[0]
        else:
            phrasel=l[1]
    except:
        h=False


    if(phrasel!='si'and phrasei!='si'):
        phrase=phrasel
    elif(phrasel!='si'):
        phrase = phrasel
    elif(phrasei!='si'):
        phrase = phrasei
    else:
        phrase = "sorry i couldn't fing anything for {query}"
    return phrase