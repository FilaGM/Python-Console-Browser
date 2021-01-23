import requests
import os
def checkPage(url):
    try:
        request = requests.get(url)
        if request.status_code == 200:
            return True
        else:
            return False
    except:
        return False

clear = lambda: os.system("cls")

def drawPage(page):
    for a in page:
        row = ""
        for b in a:
            row += b
        print(row)
        
def order(roots):
    roots.sort(key=lambda x: x["parrentId"], reverse=False)
