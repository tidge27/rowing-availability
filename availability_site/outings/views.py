from outings.forms import BookFormSet
from outings.models import Event
import datetime
from django.http import HttpResponse
from django.template import loader

def index(request):
    user = request.user
    week_commencing = datetime.date(2018,9,3)


    if request.method == "POST":
        formset = BookFormSet(request.POST, request.FILES, instance=user,
                              queryset=Event.objects.filter(start_time__lte=datetime.datetime(2040, 10, 1)),
                              date=week_commencing)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            # return HttpResponseRedirect('index.html')
    else:
        formset = BookFormSet(instance=user, queryset=Event.objects.filter(start_time__lte=datetime.datetime(2040,10, 1)),
                              date=week_commencing)

    template = loader.get_template('outings/index.html')
    context = {'formset': formset}
    return HttpResponse(template.render(context, request))