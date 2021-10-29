from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import markdown2
from random import choices,randint
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry):
    e_page = util.get_entry(entry)
    if e_page is None:
        return render(request, "encyclopedia/entry_file.html", {
            'error': "404 Not Found"
            })
    else:
        return  render(request, "encyclopedia/entry_file.html", {
            "e_title": entry,
            "e_content": e_page
            })

def search(request):
    e_title = request.GET.get('q').strip()
    if e_title in util.list_entries():
        return redirect("entry", entry=e_title)
    return render(request, "encyclopedia/search.html", {
        "entries": util.search(e_title), 
        "title": e_title
        })


def edit_page(request, entry):
    e_content = util.get_entry(entry.strip())
    if e_content == None:
        return render(request, "encyclopedia/edit_file.html", {
            'error': "404 Not Found",
            "title": entry
            })
    if request.method == "POST":
        e_content = request.POST.get("content").strip()
        if e_content == "":
            return render(request, "encyclopedia/edit_file.html", {
                "message": "Can't save with empty field.", 
                "title": entry, 
                "content": e_content})
        util.save_entry(entry, e_content)
        return redirect("entry", entry=entry)
    return render(request, "encyclopedia/edit_file.html", {
        'content': e_content, 
        'title': entry
        })


def random(request):
    e_titles = util.list_entries()
    e_title = e_titles[randint(0, len(e_titles)-1)]
    e_page = util.get_entry(e_title)
    return  render(request, "encyclopedia/entry_file.html", {
        "e_title": e_title,
        "e_content": e_page
        })

"""e_titles = util.list_entries()
    e_title = choices(e_titles)
    e_page = util.get_entry(e_title)
    return  render(request, "encyclopedia/entry_file.html", {
        "e_title": e_title,
        "e_content": e_page
        })"""

def new(request):
    if request.method == "POST":
        e_title = request.POST.get("title").strip()
        e_content = request.POST.get("content").strip()
        if e_title == "" or e_content == "":
            return render(request, "encyclopedia/new_entry.html", {
                "error": "Can't save with empty field.", 
                "title": e_title, 
                "content": e_content
                })
        if e_title in util.list_entries():
            return render(request, "encyclopedia/new_entry.html", {
                "error": "Title already exist. Try another.", 
                "title": e_title, 
                "content": e_content
                })
        util.save_entry(e_title, e_content)
        e_page = util.get_entry(e_title)
        return  render(request, "encyclopedia/entry_file.html", {
            "e_title": e_title,
            "e_content": e_page
        })
    return render(request, "encyclopedia/new_entry.html")