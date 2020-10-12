import urllib.request    #imports from standard Python library
import json

inputString = '@john @martha yo what up my peeps (smile) http://mlb.com and http://google.com'

class ParsedString:             #class ParsedString is the object that holds what will be needed for the JSON formatted string at the end
    mentions = []
    emoticons = []
    links = []
    titles = []
    wordCount = 0

def findTitle(link):                                            #function that finds the title of a webpage
    page = urllib.request.urlopen(link).read()
    title = str(page).split('<title>')[1].split('</title>')[0]
    return title

def printJSONFormat(a):                                         #formats our input string into what we're looking for
    x = {}
    if a.mentions:
        x["mentions"] = a.mentions
    if a.emoticons:
        x["emoticons"] = a.emoticons
    if a.links:
        z = []
        for i in range(len(a.links)):
            z.append({"url" : a.links[i], "title": a.titles[i]})
        x["links"] = z
    x["words"] = a.wordCount

    return(json.dumps(x, indent = 4))


def readString(input, retString):
    t = input.split()
    for i in range(len(t)):
        if t[i].startswith('@'):
            retString.mentions.append(t[i][1:])                         #adds the mention minus the @ symbol
        elif t[i].startswith('(') and t[i].endswith(')'):
            retString.emoticons.append(t[i][1:len(t[i])-1])             #adds the emoticon to the list of emoticons minus the parentheses
        elif t[i].startswith('http'):                                   #Searchs for links, then adds them to the list while also calling the title function then adding that result to the title list
            retString.titles.append(findTitle(t[i]))
            retString.links.append(t[i])
        else:
            retString.wordCount+=1

retString = ParsedString()

readString(inputString, retString)
retString = printJSONFormat(retString)
print(retString)