from django.shortcuts import render
import random
from . import util
import markdown

def converter(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    htmlcontent = converter(title)
    if htmlcontent == None:
        return render (request, "encyclopedia/Error_Page.html")
    else:
        return render (request, "encyclopedia/entry.html",{
            "title":title,
            "content":htmlcontent
        })

def search(request):
    
    if request.method == "POST":
        entrysearch = request.POST['q']
        htmlcontent = converter(entrysearch)
        if htmlcontent != None:
            return render (request,"encyclopedia/entry.html",{
                "title": entrysearch,
                "content":htmlcontent
            })
        else:
            allEntries = util.list_entries()
            suggestions = []
            for entry in allEntries:
                if entrysearch.lower() in entry.lower():
                    suggestions.append(entry)
            return render (request, "encyclopedia/suggest.html",{
                "suggestions" : suggestions
            })    
        
def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")



def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST ['content']
        existence = util.get_entry(title)
        if existence != None:
            return render(request,"encyclopedia/Error_Page.html",{
                "message":"Entry page already exists"
            })
        else:
            util.save_entry(title,content)
            htmlcontent = converter(title)
            return render(request,"encyclopedia/pagesave.html",{
                "title": title,
                "content": htmlcontent,
            })

def edit(request):
    if request.method == "POST":
        title = request.POST['entrytitle']
        content = util.get_entry(title) 
        
        return render(request, "encyclopedia/edit.html",{
            "title":title,
            "content":content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST ['content']
        util.save_entry(title,content)
        htmlcontent = converter(title)
        return render(request,"encyclopedia/entry.html",{
                "title": title,
                "content": htmlcontent,
            })
    
def randomiser(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    content = converter(entry)
    return render(request, "encyclopedia/entry.html",{
        "title": entry,
        "content":content
    })
