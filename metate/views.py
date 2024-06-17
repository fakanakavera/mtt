from django.shortcuts import render

# Create your views here.
def index(request):
    # return blank response
    return render(request, 'metate/index.html')