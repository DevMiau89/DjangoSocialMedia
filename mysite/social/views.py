from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

def index_nav(request):
    return render(request, 'index_nav.html', {})
