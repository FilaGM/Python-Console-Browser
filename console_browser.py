import os
import requests
import time
from html.parser import HTMLParser
from libs.functions import clear,checkPage,drawPage,order

boxes = ["div","center","ul"]

class ConsoleHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global id,roots,getVal
        if tag in boxes:
            roots[-1]["children"].append({
                "tag":tag,
                "args":attrs,
                "id":id,
                "parrentId":roots[-1]["id"],
                "children":[]
            })
            roots.append(roots[-1]["children"][-1])
        else:
            roots[-1]["children"].append({
                "tag":tag,
                "args":attrs,
                "content":None,
                "id":id,
                "parrentId":roots[-1]["id"]
            })
            getVal = True
        id += 1 

    def handle_endtag(self, tag):
        global roots,roots2
        if tag == roots[-1]["tag"]:
            roots2.append(roots[-1])
            roots.remove(roots[-1])

    def handle_data(self, data):
        global getVal
        if getVal == True:
            roots[-1]["children"][-1]["content"] = data
            getVal = False

parser = ConsoleHTMLParser()


while True:
    size = os.get_terminal_size()

    charWidth = size.columns
    charHeight = size.lines

    clear()
    print("Terminal browser inicialized.")
    print("Size: "+str(charWidth)+"x"+str(charHeight))

    url = input("Browse url:")
    print()
    print("Checking page...")

    if checkPage(url):
        while True:
            print()
            print("Loading page...")
            page = requests.get(url)
            id = 0
            root = {
                "tag":"root",
                "id":id,
                "parrentId":-1,
                "children":[]
            }
            id += 1
            roots = []
            roots.append(root)
            roots2 = []
            roots2.append(root)
            getVal = False
            parser.feed(page.text)
            order(roots2)
            for a in roots2:
                print(a["tag"])
                for b in a.items():
                    if b[0] != "tag" and b[0] != "children":
                        print("---"+str(b))
                    elif b[0] == "children":
                        for c in b[1]:
                            dontShow = ["script","style","div","center"]
                            if not c["tag"] in dontShow:
                                print("------"+str(c))
                        
                print("")
            input()
            break
    else:
        print("Page doesnt exist.")
        time.sleep(1)
        continue
