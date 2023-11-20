from django.shortcuts import render, redirect, get_object_or_404
import uuid
from .models import Url
from django.http import HttpResponse
import datetime
from django.utils import timezone
import pytz


def index(request):
    return render(request, 'index.html')

def create(request):
    try:
        if request.method == 'POST':
            link = request.POST['link']
            expiration_date = request.POST.get("expiration_date") or timezone.now() + timezone.timedelta(days=30)

            if link :
                if link.startswith('localhost'):
                    return HttpResponse("Given link cannot be shorten further.")
                
                link_in_db = Url.objects.filter(link=link)

                if link_in_db.exists():
                    return HttpResponse("localhost:8000/" + link_in_db[0].uuid)
                
                uid = str(uuid.uuid4())[:5]
                new_url = Url(link=link,uuid=uid, expiration_date=expiration_date)
                new_url.save()
                return HttpResponse(f"localhost:8000/{uid}")
            return HttpResponse("Please provide the valid link.")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
        

def go(request, pk):
    try:
        url_details =  get_object_or_404(Url, uuid=pk)

        expiration_date_local = url_details.expiration_date.astimezone(timezone.get_current_timezone())
        # expiration_date_local = expiration_date_local.replace(tzinfo=None)
        now_local = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if str(expiration_date_local) < now_local:
            url_details.delete()
            return HttpResponse("Link has expired.")
        
        if url_details:
            return redirect(url_details.link)
        
    except Url.DoesNotExist:
        return HttpResponse("Page not found.....")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    

def delete(request):
    try:
        if request.method == "DELETE":
            short_url = request.GET['link']
            uid = short_url.split('/')[-1]

            url_details = Url.objects.filter(uuid=uid)

            if url_details:
                url_details.delete()
                return HttpResponse("Link deleted successfully.")
            else:
                return HttpResponse("Link does not exist.")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
    

def extend_validity(request):
    try:
        # check for expiry date, if its already expire delete the link
        # else extend expiry date till given date
        short_url = request.POST['link']
        uid = short_url.split('/')[-1]
        url_details =  Url.objects.get(uuid=uid)

        expiration_date_local = url_details.expiration_date.astimezone(timezone.get_current_timezone())
        expiration_date_local = expiration_date_local.replace(tzinfo=None)
        now_local = timezone.now().replace(tzinfo=None)

        if expiration_date_local < now_local:
            url_details.delete()
            return HttpResponse("Link has already expired.")
        
        new_expiration_date = request.POST.get("expiration_date")

        if new_expiration_date:
            # new_expiration_date = timezone.make_aware(timezone.datetime.strptime(new_expiration_date, '%Y-%m-%d %H:%M:%S'))
            url_details.expiration_date = new_expiration_date
            url_details.save()
            return HttpResponse(f"Url now is valid till {new_expiration_date}")
        else:
            return HttpResponse("Please provide expiry date.")
    except Exception as e:
        return HttpResponse(f"Error: {e}")