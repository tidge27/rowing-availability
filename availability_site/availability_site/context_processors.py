def base_context(request):
    my_context = {
        "user": request.user if request.user.is_authenticated else {'email': "Logged Out"},
        "login_logout_text": "Logout" if request.user.is_authenticated else "Login with Raven",
        "login_logout_link": "/logout/raven" if request.user.is_authenticated else "/login/raven",
        "pages": [
            {
                "name": "Home",
                "icon": "home",
                "link": "/",
            },
            {
                "name": "Availabilities",
                "icon": "calendar_today",
                "link": "/outings/availabilities"
            },
            {
                "name": "Outings",
                "icon": "access_time",
                "link": "/outings/outings"
            }
        ],
        "admin_pages": [
            {
                "name": "Groups",
                "icon": "group",
                "link": "/groups/groups",
            },
        ],
        "support_email":"mailto:tidge27@gmail.com"
    }
    return my_context