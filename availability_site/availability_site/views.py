from django.http import HttpResponse
from django.template import loader, Context

def index(request):
    template = loader.get_template('index.html')
    my_context = {
        "user": request.user if request.user.is_authenticated else {'email': "Logged Out"},
        "login_logout_text": "Logout" if request.user.is_authenticated else "Login with Raven",
        "login_logout_link": "/logout/raven" if request.user.is_authenticated else "/login/raven",
        "pages": [
            {
                "name": "Home",
                "icon": "home",
                "link": "#",
            },
            {
                "name": "Availabilities",
                "icon": "calendar_today",
                "link": "/outings/availabilities"
            }
        ],
        "support_email":"mailto:tidge27@gmail.com"
    }
    return HttpResponse(template.render(my_context, request))