import re, math
# import requests
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
        # return requests.get(url).content
        return urlopen(url).read()
    except:
        return ""
        
def smlr(text):
    start = text.index('<p><b>')
    end = text.index('toctitle')
    if start == -1 or end == -1:
        return text
    return text[start:end]

def get_next_link(text, start, target_vector, target_url):
    ahref = text.find('<a href="/wiki', start)
    if ahref == -1: 
        return None, -1, 0
    first = ahref + 9
    last = text.find('"', first)
    # short_sentence = text[first-100 if first >= 100 else first:last+100]
    short_sentence = text[first:last]
    vector = text_to_vector(short_sentence)
    score = get_cosine(vector, target_vector)
    url_near_match = get_cosine(vector, text_to_vector(target_url))
    if url_near_match >= 0.50:
        score = url_near_match
    return "http://en.wikipedia.org" + text[first:last], last, score

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

def get_all_links(url, page, target_url, target_vector, links, depth, todo):
    # links = []
    position = 0
    score = 0
    while True:
        link, position, score = get_next_link(page, position, target_vector, target_url)
        if link == None:
            break
        # if link.find(':', 5) != -1:
        #     # print link
        #     continue
        # if link.find('.wikipedia.org',28) != -1:
        #     continue
        if extraneous(link):
            continue
        match = False
        for i in links:
            if link == i['url']:
                match = True
                break
        if match:
            continue
        links.append({'url': link, 'score': score, 'parent':url, 'depth':depth, 'visited':False})
        todo.append(link)
        if link == target_url:
            # print True
            return links, True
        # page = page[position:]
    # print False
    return links, False

def best_search(start_url, target_url, max_depth=20):
    if start_url == target_url: 
        return [start_url], 0
    todo = [start_url]
    # visited = [start_url]
    links = [{'url':start_url, 'score':0, 'parent':None, 'depth':0, 'visited':False}]
    # depth = 0
    target_vector = text_to_vector(get_page(target_url))
    while todo:
        links = sorted(links, key=lambda k: k['score'], reverse=True)
        # print links
        # best = links[0]
        for i in links:
            if i['visited'] == False:
                i['visited'] = True
                best = i
                print 'best:', best
                break
        depth = best['depth']
        if depth > max_depth:
            continue
        url = best['url']
        # print url
        # print todo
        todo.pop(todo.index(url))
        # print url
        contents = get_page(url)
        links, boo = get_all_links(url, contents, target_url, target_vector, links, depth + 1, todo)
        if boo:
            path = [target_url]
            parent = target_url
            while path[0] != start_url:
                for i in links:
                    if i['url'] == parent:
                        parent = i['parent']
                        break
                # prev = (item for item in links if item["parent"] == parent).next()
                # parent = prev['parent']
                path.insert(0,parent)
            return path, len(path) - 1
    # return "No path given max depth", -1
    return ["Error: Path unavailable"], -1



# u1 = 'http://en.wikipedia.org/wiki/Kobe_Bryant'
# u2 = 'http://en.wikipedia.org/wiki/Underwater_basket_weaving'
# print best_search(u1, u2)


# url = 'http://en.wikipedia.org/wiki/Kobe_Bryant'
# page = get_page(url)
# target_url = 'http://en.wikipedia.org/wiki/Pittsburgh'
# target_vector = text_to_vector(get_page(target_url))
# links, boo = get_all_links(url, page, target_url, target_vector, [], 0, [])
# newlinks = sorted(links, key=lambda k: k['score'], reverse=True)
# print newlinks
# print boo


# text1 = smlr(get_page('http://en.wikipedia.org/wiki/Kobe_Bryant'))
# text2 = 'Kobe Bryant was born in Philadelphia, Pennsylvania.'

# vector1 = text_to_vector(text1)
# vector2 = text_to_vector(text2)

# cosine = get_cosine(vector1, vector2)

# print 'Cosine:', cosine

