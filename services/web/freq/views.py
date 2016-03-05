from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello.\n', content_type='text/plain')
