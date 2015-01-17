import re, math
from urllib import *
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

def get_page(url):
    try:
        return urlopen(url).read()
    except:
        return ""
        
def smlr(text):
    start = text.index('<p><b>')
    end = text.index('toctitle')
    if start == -1 or end == -1:
        return text
    return text[start:end]

def extraneous(link):
    if link.find(':', 5) != -1:
        return True
    if link.find('.wikipedia.org',28) != -1:
        return True
    if link.find('.',29,30) != -1:
        return True
    bad = [
            "http://en.wikipedia.org/wiki/Main_Page",
            "http://en.wikipedia.org/wiki/Virtual_International_Authority_File",
            "http://en.wikipedia.org/wiki/Library_of_Congress_Control_Number",
            "http://en.wikipedia.org/wiki/International_Standard_Book_Number"
    ]
    if link in bad: 
        return True
    return False

def get_next_link(text, init_pos):
    ahref = text.find("""<a href="/wiki/""", init_pos)
    if ahref == -1:
        return "", -1
    first = ahref + 9
    last = text.find('"', first)
    return "http://en.wikipedia.org" + text[first:last], last

def get_all_links(url, dic):
    text = get_page(url)
    init_pos = 0
    arr = []
    while True:
        link, init_pos = get_next_link(text, init_pos)
        if link == "":
            break
        if extraneous(link):
            continue
        arr.append(link)
        if link in dic:
            continue
        dic[link] = url
    return arr

def search(u1, u2, dic1, dic2):
    if u1 == u2:
        return [u1]
    links1 = get_all_links(u1, dic1)
    links2 = get_all_links(u2, dic2)
    keys_1 = set(dic1.keys())
    keys_2 = set(dic2.keys())
    intersection = list(keys_1 & keys_2)
    if intersection:
        print intersection
        intersection_link = intersection[0]
        # intersection_link = intersection[len(intersection)-1]
        back = [intersection_link]
        forward = []
        running_back_link = intersection_link
        running_forward_link = intersection_link
        back_boo = True
        forward_boo = True
        while back_boo or forward_boo:
            if back_boo == True:
                if running_back_link in dic1:
                    running_back_link = dic1[running_back_link]
                    back.insert(0, running_back_link)
                    if running_back_link == None:
                        back_boo = False
                        back = back[1:]
            if forward_boo == True:
                if running_forward_link in dic2:
                    running_forward_link = dic2[running_forward_link]
                    forward.append(running_forward_link)
                    if running_forward_link == None:
                        forward_boo = False
                        forward = forward[:-1]
        return back + forward
    else:
        best = 0.0
        best1 = ""
        best2 = ""
        # links1 = map(text_to_vector, links1)
        # links2 = map(text_to_vector, links2)
        for link1 in links1:
            for link2 in links2:
                score = get_cosine(text_to_vector(link1), text_to_vector(link2))
                # score = get_cosine(link1, link2)
                if score > best:
                    best = score
                    best1 = link1
                    best2 = link2
        return search(best1, best2, dic1, dic2)


# u1 = """http://en.wikipedia.org/wiki/List_of_films_that_most_frequently_use_the_word_"fuck"""""
# u2 = """http://en.wikipedia.org/wiki/Testicle_Festival"""
# dic1 = {u1: None}
# dic2 = {u2: None}
# print search(u1, u2, dic1, dic2)