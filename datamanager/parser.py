# -*- coding: utf-8 -*-
import re
import urllib2
from bs4 import BeautifulSoup
from bs4 import Comment
from bs4 import Tag

NEGATIVE = re.compile(".*comment.*|.*meta.*|.*footer.*|.*foot.*|.*cloud.*|.*head.*")
POSITIVE = re.compile(".*post.*|.*hentry.*|.*entry.*|.*content.*|.*text.*|.*body.*")
BR = re.compile("<br */? *>[ \r\n]*<br */? *>")

def extract_content_with_Arc90(html):

    soup = BeautifulSoup( re.sub(BR, "</p><p>", html) )

    soup = simplify_html_before(soup)
    topParent = None
    parents = []
    for paragraph in soup.findAll("p"):

        parent = paragraph.parent

        if (parent not in parents):
            parents.append(parent)
            parent.score = 0

            if (parent.has_key("class")):
                if (NEGATIVE.match(str(parent["class"]))):
                    parent.score -= 50
                elif (POSITIVE.match(str(parent["class"]))):
                    parent.score += 25

            if (parent.has_key("id")):
                if (NEGATIVE.match(str(parent["id"]))):
                    parent.score -= 50
                elif (POSITIVE.match(str(parent["id"]))):
                    parent.score += 25

        if (len( paragraph.renderContents() ) > 10):
            parent.score += 1

        # you can add more rules here!

    topParent = max(parents, key=lambda x: x.score)
    simplify_html_after(topParent)
    if ("\n\n\n") in topParent.text:
        return exceptionBody(soup)
    else:
        return topParent.text

def simplify_html_after(soup):

    for element in soup.findAll(True):
        element.attrs = {}
        if( len( element.renderContents().strip() ) == 0 ):
            element.extract()
    return soup

def simplify_html_before(soup):

    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]

    # you can add more rules here!

    map(lambda x: x.replaceWith(x.text.strip()), soup.findAll("li"))    # tag to text
    map(lambda x: x.replaceWith(x.text.strip()), soup.findAll("em"))    # tag to text
    map(lambda x: x.replaceWith(x.text.strip()), soup.findAll("tt"))    # tag to text
    map(lambda x: x.replaceWith(x.text.strip()), soup.findAll("b"))     # tag to text

    replace_by_paragraph(soup, 'blockquote')
    replace_by_paragraph(soup, 'quote')

    map(lambda x: x.extract(), soup.findAll("code"))      # delete all
    map(lambda x: x.extract(), soup.findAll("style"))     # delete all
    map(lambda x: x.extract(), soup.findAll("script"))    # delete all
    map(lambda x: x.extract(), soup.findAll("link"))      # delete all

    delete_if_no_text(soup, "td")
    delete_if_no_text(soup, "tr")
    delete_if_no_text(soup, "div")

    delete_by_min_size(soup, "td", 10, 2)
    delete_by_min_size(soup, "tr", 10, 2)
    delete_by_min_size(soup, "div", 10, 2)
    delete_by_min_size(soup, "table", 10, 2)
    delete_by_min_size(soup, "p", 50, 2)

    return soup

def delete_if_no_text(soup, tag):

    for p in soup.findAll(tag):
        if(len(p.renderContents().strip()) == 0):
            p.extract()

def delete_by_min_size(soup, tag, length, children):

    for p in soup.findAll(tag):
        if(len(p.text) < length and len(p) <= children):
            p.extract()

def replace_by_paragraph(soup, tag):

    for t in soup.findAll(tag):
        t.name = "p"
        t.attrs = {}

def extractLink(response):
    extractUrlList = []
    soup = BeautifulSoup(response)
    for link in soup.findAll('a'):
        extractUrlList.append(link)
    return extractUrlList

def extractTitle(soup):
     titleText = soup.find('title').string
     return titleText

def extractDate(soup):
    valueTime = soup.find("p", {'class':'date'})
    dateParser = re.compile('<em>([0-9.: ]+)</em>', re.S|re.I)
    try :
        returnTime = dateParser.search(str(valueTime)).group(1).strip()
        return returnTime
    except Exception, e:
        return soup.find("span", {'class':'time'}).text

def exceptionBody(soup):
    map(lambda x: x.extract(), soup.findAll("code"))
    map(lambda x: x.extract(), soup.findAll("script"))
    map(lambda x: x.extract(), soup.findAll("pre"))
    map(lambda x: x.extract(), soup.findAll("style"))
    map(lambda x: x.extract(), soup.findAll("embed"))

    comments = soup.findAll(text=lambda text:isinstance(text, Comment))

    [comment.extract() for comment in comments]

    white_string = ""
    isIn = False;

    for character in soup.prettify():
        if character == "<":
            isIn = True;
        if isIn:
            white_string += " "
        else:
            white_string += character
        if character == ">":
            isIn = False;

    resultStr = ""
    for string in white_string.split("           "):    # tune here!
        p = string.strip()
        p = re.sub(' +',' ', p)
        p = re.sub('\n+',' ', p)
        if (len(p.strip()) > 40) and string.count('\n') < 3:
            resultStr = resultStr + p.strip()
    return resultStr
