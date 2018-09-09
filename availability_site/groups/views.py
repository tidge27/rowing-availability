from django.forms import modelformset_factory
from django.shortcuts import render
from groups.models import Group, GroupMember
from groups.forms import GroupModelForm, GroupMemberFormSet
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic.list import ListView

class GroupListView(ListView):
    model = Group
    context_object_name = "group_list"
    template_name = 'groups/manage_group.html'

def create_group(request):
    group_form = GroupModelForm()
    group = Group()
    if request.method == "POST":
        group = GroupModelForm(request.POST)
        if group.is_valid():
            created_group = group.save()
        formset = GroupMemberFormSet(request.POST, instance=created_group)
        if formset.is_valid():
            formset.save()

    else:
        formset = GroupMemberFormSet(instance=group)

    template = loader.get_template('groups/create_update.html')
    context = {
        'group_form': group_form,
        'formset': formset,
    }
    return HttpResponse(template.render(context, request))