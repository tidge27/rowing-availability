from outings.forms import BookFormSet
from outings.models import Event
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from dateutil.relativedelta import relativedelta, MO

def availabilities(request):
    user = request.user
    print(request.GET.get("date", "05052018"))
    try:
        week_commencing = datetime.datetime.strptime(request.GET.get("date", ""), "%d%m%Y")
    except Exception as e:
        now = datetime.datetime.now()
        week_commencing = datetime.datetime(now.year, now.month, now.day, 0, 0, 0) + relativedelta(weekday=MO(-1))
    prev_monday = datetime.datetime.strftime(week_commencing + relativedelta(weekday=MO(-2)), "%d%m%Y")
    prev_monday_link = "?date={}".format(prev_monday)
    next_monday = datetime.datetime.strftime(week_commencing + relativedelta(weekday=MO(2)), "%d%m%Y")
    next_monday_link = "?date={}".format(next_monday)

    if request.method == "POST":
    # if False:
        formsets=[]
        for i in range(0,6):
            start_of_day = week_commencing + datetime.timedelta(days=i)
            end_of_day = week_commencing + datetime.timedelta(days=i+1)
            formsets.append(BookFormSet(request.POST, request.FILES, prefix="set_{}".format(i), instance=user,
                              queryset=Event.objects.filter(start_time__gte=start_of_day, start_time__lte=end_of_day),
                              date=week_commencing+ datetime.timedelta(days=i)))
        all_valid = True
        for formset in formsets:
            if formset.is_valid():
                pass
            else:
                all_valid = False
        if all_valid:
            for formset in formsets:
                formset.save()
            formsets = []
            for i in range(0, 6):
                start_of_day = week_commencing + datetime.timedelta(days=i)
                end_of_day = week_commencing + datetime.timedelta(days=i + 1)
                formsets.append(BookFormSet(prefix="set_{}".format(i), instance=user,
                                            queryset=Event.objects.filter(start_time__gte=start_of_day,
                                                                          start_time__lte=end_of_day),
                                            date=week_commencing + datetime.timedelta(days=i)))
            # Do something. Should generally end with a redirect. For example:
            # return HttpResponseRedirect('')
    else:
        formsets = []
        for i in range(0, 6):
            start_of_day = week_commencing + datetime.timedelta(days=i)
            end_of_day = week_commencing + datetime.timedelta(days=i+1)
            formsets.append(BookFormSet(prefix="set_{}".format(i), instance=user,
                                        queryset=Event.objects.filter(start_time__gte=start_of_day,
                                                                      start_time__lte=end_of_day),
                                        date=week_commencing+ datetime.timedelta(days=i)))

    template = loader.get_template('outings/availabilities.html')
    context = {'formsets': formsets,
               'prev_monday_link': prev_monday_link,
               'next_monday_link': next_monday_link,
               }
    return HttpResponse(template.render(context, request))

# def index(request):
#     user = request.user
#     week_commencing = datetime.date(2018,9,3)
#
#
#     if request.method == "POST":
#         formset = BookFormSet(request.POST, request.FILES, instance=user,
#                               queryset=Event.objects.filter(start_time__lte=datetime.datetime(2040, 10, 1)),
#                               date=week_commencing)
#         if formset.is_valid():
#             formset.save()
#             # Do something. Should generally end with a redirect. For example:
#             # return HttpResponseRedirect('index.html')
#     else:
#         formset = BookFormSet(instance=user, queryset=Event.objects.filter(start_time__lte=datetime.datetime(2040,10, 1)),
#                               date=week_commencing)
#
#     template = loader.get_template('outings/index.html')
#     context = {'formset': formset}
#     return HttpResponse(template.render(context, request))