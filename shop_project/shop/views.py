from django.shortcuts import render

# This is your homepage view
def home(request):
    return render(request, 'home.html')
