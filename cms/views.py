from django.shortcuts import render

from cms.models import News


# Create your views here.


def home(request):
    latest_news = News.objects.all().order_by('-created_at')[:20]

    context = {}

    if latest_news.exists():
        context['principal'] = latest_news[0]
        context['latest_news'] = latest_news[1:13] if len(latest_news) > 1 else []
    else:
        context['principal'] = None
        context['latest_news'] = []

    return render(request, 'cms/home.html', context)
