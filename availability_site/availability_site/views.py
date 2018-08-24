from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('index.html')
    context = {
        "user": request.user if request.user.is_authenticated else {'email': "Logged Out"},
        "login_logout_text": "Logout" if request.user.is_authenticated else "Login with Raven",
        "login_logout_link": "/logout" if request.user.is_authenticated else "/login"
    }
    return HttpResponse(template.render(context, request))