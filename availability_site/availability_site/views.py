from django.http import HttpResponse
from django.template import loader, Context

def index(request):
    template = loader.get_template('index.html')
    my_context = {
    }
    return HttpResponse(template.render(my_context, request))