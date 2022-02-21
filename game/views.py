from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def room(request, room_code):
    return render(request, 'index.html', {
        'room_code': room_code
    })