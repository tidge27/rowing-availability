from outings.forms import BookFormSet
from outings.models import Event, Outing, OutingMember
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from dateutil.relativedelta import relativedelta, MO
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.views.generic.base import TemplateView
import json
from groups.models import GroupMember, Group

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
        print(json.dumps(request.POST))
        formsets=[]
        for i in range(0,7):
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
            for i in range(0, 7):
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
        for i in range(0, 7):
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

class UserOutingMemberListView(ListView):
    model = OutingMember
    queryset = OutingMember.objects.filter(outing__start_time__gte=datetime.datetime.now()).order_by('outing__start_time')
    context_object_name = 'outing_list'
    template_name = 'outings/outings.html'
    # paginate_by = 100  # if pagination is desired

    def get_queryset(self):
        queryset = super(UserOutingMemberListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context

class UserOutingDetailView(DetailView):
    model = Outing
    context_object_name = 'outing'
    template_name = 'outings/outing.html'


class CombinedAvailabilityView(TemplateView):
    template_name = 'outings/group-availabilities.html'

    def get(self, request, *args, **kwargs):
        try:
            day = datetime.datetime.strptime(request.GET.get("date", ""), "%d%m%Y")
            day = day.replace(tzinfo=datetime.timezone.utc)
        except Exception as e:
            print(e)
            today_now = datetime.datetime.now()
            day = datetime.datetime(today_now.year, today_now.month, today_now.day, 0, 0, 0, tzinfo=datetime.timezone.utc)

        prev_day = datetime.datetime.strftime(day + relativedelta(days=1), "%d%m%Y")
        prev_day_link = "?date={}".format(prev_day)
        next_day = datetime.datetime.strftime(day + relativedelta(days=1), "%d%m%Y")
        next_day_link = "?date={}".format(next_day)

        import untangle
        lighting_down = day
        lighting_up = day + datetime.timedelta(hours=24)
        lighting_times = untangle.parse("lightings.xml")
        for each_day in lighting_times.lightings_data.lightings:
            if each_day.date.cdata == datetime.datetime.strftime(day, "%Y%m%d"):
                print("found today's lighting times!")
                lighting_down = datetime.datetime.fromtimestamp(int(each_day.timestamp_down.cdata), tz=datetime.timezone.utc)
                lighting_up= datetime.datetime.fromtimestamp(int(each_day.timestamp_up.cdata), tz=datetime.timezone.utc)
                print(lighting_up, lighting_down)





        group = self.request.GET.get("group", None)
        print(group)
        groupmembers = GroupMember.objects.filter(group__name=group)
        users= []
        for memb in groupmembers:
            users.append(memb.user)

        # NOTE will need to incorporate the lighting up/down timings here
        # TODO look into using agregate

        now = day
        end = now + datetime.timedelta(hours=24) - datetime.timedelta(minutes=1)
        time_list = [end]

        print(Event.objects.filter(
            user__in=users, start_time__gte=now, start_time__lte=end
        ).values_list('start_time', flat=True))

        time_list.extend(Event.objects.filter(
            user__in=users, start_time__gte=now, start_time__lte=end
        ).values_list('start_time', flat=True))
        time_list.extend(Event.objects.filter(
            user__in=users, end_time__gte=now, end_time__lte=end
        ).values_list('end_time', flat=True))

        time_list.append(lighting_down)
        time_list.append(lighting_up)
        time_list.sort()

        print(time_list)



        new_user_busy_list = []
        for user in users:
            if user.is_busy(time=now):
                new_user_busy_list.append(user)
        new_user_busy_list.append({"crsid": "Lighting"})
        old_user_busy_list = []
        time_block_list = [
            {'start_time': now,
             'end_time': now,
             'users': new_user_busy_list,
             }
        ]
        block_index = 0
        # while now < end:
        for now in time_list:
            old_user_busy_list = new_user_busy_list
            new_user_busy_list = []
            for user in users:
                if user.is_busy(now):
                    new_user_busy_list.append(user)
            if not lighting_down <= now < lighting_up:
                new_user_busy_list.append({"crsid": "Lighting"})

            if new_user_busy_list != old_user_busy_list:
                print("someone has changed availability")
                time_block_list[block_index]['end_time'] = now
                time_block_list.append(
                    {'start_time': now,
                     'end_time': now,
                     'users': new_user_busy_list,
                     }
                )
                block_index += 1
            # now += datetime.timedelta(minutes=1)
        time_block_list[block_index]['end_time'] = end

        print(time_block_list)

        for time in time_block_list:
            time['length_mins'] = (time['end_time'] - time['start_time']).total_seconds()/60
            print(time['length_mins'])
            time['length_percent'] = (time['length_mins']/1440.0)*100.0

            if time['users'] == []:
                time['html_color'] = "rgb(139, 195, 74)"
            elif len(time['users']) == 1:
                time['html_color'] = "rgb(255, 193, 7)"
            else:
                time['html_color'] = "rgb(255, 152, 0)"



        template = loader.get_template('outings/group-availabilities.html')
        context = {'time_block_list': time_block_list,
                   'group': group,
                   'availability_day': day,
                   'prev_day_link': prev_day_link,
                   'next_day_link': next_day_link}
        return HttpResponse(template.render(context, request))
