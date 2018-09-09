from django.forms import inlineformset_factory, ModelForm, modelformset_factory
from django import forms
from groups.models import GroupMember, Group
from users.models import MyUser
from datetime import datetime


class GroupMemberForm(ModelForm):

    class Meta:
        model = GroupMember
        fields = ['seat']

BaseGroupMemberFormSet = inlineformset_factory(Group, GroupMember, form=GroupMemberForm)

class GroupMemberFormSet(BaseGroupMemberFormSet):
    pass


class GroupModelForm(ModelForm):

    class Meta:
        model = Group
        fields = ['name']