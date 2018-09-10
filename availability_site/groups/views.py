from django.forms import modelformset_factory
from django.shortcuts import render
from groups.models import Group, GroupMember
from groups.forms import GroupModelForm, GroupMemberFormSet
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic.list import ListView
from django.urls import reverse

class GroupListView(ListView):
    model = Group
    context_object_name = "group_list"
    template_name = 'groups/manage_group.html'

def create_group(request):
    if request.GET.get("id", None):
        group = Group.objects.get(id=request.GET.get("id", None))
    else:
        group = Group()

    if request.method == "POST":
        group = GroupModelForm(request.POST, instance=group)
        if group.is_valid():
            created_group = group.save()
            formset = GroupMemberFormSet(request.POST, instance=created_group)
            print(formset)
            if formset.is_valid():
                formset.save()
                print(formset.cleaned_data)
                return HttpResponseRedirect(reverse('groups'))


            else:
                print("formset invalid")
                print(formset.errors)
                context = {
                    'group_form': group,
                    'formset': formset,
                }
        else:
            print("form invalic")
            formset = GroupMemberFormSet(instance=Group())
            context = {
                'group_form': group,
                'formset': formset,
            }


    else:

        if request.GET.get("id", None):
            group = Group.objects.get(id=request.GET.get("id", None))
            group_form = GroupModelForm(instance=group)
        else:
            group = Group()
            group_form = GroupModelForm()

        formset = GroupMemberFormSet(instance=group)

        context = {
            'group_form': group_form,
            'formset': formset,
        }
    template = loader.get_template('groups/create_update.html')
    return HttpResponse(template.render(context, request))