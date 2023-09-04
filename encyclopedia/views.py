from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
import random
import markdown
from django.shortcuts import redirect
from django import forms
from . import util 

class EditPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="Content", widget=forms.Textarea)

def convert_md_to_html(title):
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
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": html_content
        })


def search(request):
    if request.method == "POST":
        searches = request.POST.get("q")
        html_content = convert_md_to_html(searches)

        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": searches,
                "content": html_content
            })
        else:
            allEntries = util.list_entries()
            recommendations = []

            for entry in allEntries:
                if searches.lower() in entry.lower():
                    recommendations.append(entry)

            if recommendations:
                return render(request, "encyclopedia/search.html", {
                    "recommendations": recommendations
                })

    # If no matches were found or it's not a POST request, render a default template
    return render(request, "encyclopedia/index.html")


    
def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        title_exist = util.get_entry(title)

        if title_exist is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)  # Call the function with the title parameter
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })
    else:
        # Handle GET request (display the form for creating a new entry)
        return render(request, "encyclopedia/new_page.html")

    

def edit_page(request):
    if request.method == "POST":
        new_title = request.POST.get('entry_title')
        entry_content = util.get_entry(new_title)
        return render(request, "encyclopedia/edit_page.html", {
            "title": new_title,
            "content": entry_content
        })
    else:
        # Handle GET request (e.g., when navigating to the edit page)
        return HttpResponse("This is the edit page for viewing and editing entries.")



def save_edit(request):
    if request.method == "POST":
        title = request.POST.get("title", "")  # Use get with a default value
        content = request.POST.get("content", "")  # Use get with a default value

        if title:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title, 
                "content": html_content
            })
        else:
            # Handle the case where 'title' is missing
            # You can return an error message or redirect as needed
            return render(request, "encyclopedia/error.html", {
                "message": "Title is missing"
            })


def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    html_content = convert_md_to_html(random_entry)  # Call the function with the random entry title
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })








