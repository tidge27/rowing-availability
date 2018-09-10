from django.forms import inlineformset_factory, ModelForm, modelformset_factory
from django import forms
from groups.models import GroupMember, Group
from users.models import MyUser
from datetime import datetime


class GroupMemberForm(ModelForm):

    class Meta:
        model = GroupMember
        fields = ['seat', 'user']

BaseGroupMemberFormSet = inlineformset_factory(Group, GroupMember, form=GroupMemberForm, extra=10, max_num=9)

class GroupMemberFormSet(BaseGroupMemberFormSet):
    def __init__(self, *args, **kwargs):
        super(GroupMemberFormSet, self).__init__(*args, **kwargs)
        self.queryset = self.queryset.order_by('-seat')


class GroupModelForm(ModelForm):

    class Meta:
        model = Group
        fields = ['name']