from django.shortcuts import render, redirect
import uuid
from .models import Url
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')

def create(request):
    if request.method == 'POST':
        link = request.POST['link']
        if link :
            if link.startswith('localhost'):
                return HttpResponse("Given link cannot be shorten further.")
            link_in_db = Url.objects.filter(link=link)
            if link_in_db.exists():
                return HttpResponse(link_in_db[0].uuid)
            uid = str(uuid.uuid4())[:5]
            new_url = Url(link=link,uuid=uid)
            new_url.save()
            return HttpResponse("localhost:8000/" + uid)
        return HttpResponse("Please provide the valid link.")

def go(request, pk):
    try:
        url_details = Url.objects.get(uuid=pk)
        if url_details:
            return redirect(url_details.link)
    except:
        return HttpResponse("Page not found.")
    
def delete(request):
    try:
        if request.method == "DELETE":
            short_url = request.GET['link']
            uid = short_url.split('/')[-1]
            url_details = Url.objects.get(uuid=uid)
            if url_details:
                Url.objects.filter(uuid=uid).delete()
                return HttpResponse("Link deleted successfully.")
            return HttpResponse("Link does not exist.")
    except:
        return HttpResponse("Link does not exist.")