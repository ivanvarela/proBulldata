from django.shortcuts import render

from cms.models import News


# Create your views here.


def home(request):
    latest_news = News.objects.all().order_by('-created_at')[:20]

    context = {
        'principal': latest_news[0],
        'latest_news': latest_news[1:13],
    }
    return render(request, 'cms/home.html', context)
