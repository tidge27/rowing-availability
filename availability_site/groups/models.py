from django.db import models
import uuid
from users.models import MyUser


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=140)
    is_boat = models.BooleanField(default=False)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('group-detail', args=[str(self.id)])

    @property
    def get_member_count(self):
        return len(GroupMember.objects.filter(group=self))

    def __str__(self):
        return '<Group {}>'.format(self.name)




class GroupMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    seat = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '<Group member {}>'.format(self.seat)
