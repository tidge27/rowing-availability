from django.contrib import admin
from groups.models import Group, GroupMember

admin.site.register(Group)
admin.site.register(GroupMember)