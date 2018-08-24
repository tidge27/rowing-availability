from django.db import models
import uuid
from users.models import MyUser
from groups.models import Group


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return '<Event {} - {}>'.format(self.start_time, self.end_time)


class Outing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return '<Outing at {}>'.format(self.start_time)


class OutingMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    outing = models.ForeignKey(Outing, on_delete=models.CASCADE)
    seat = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '<Outing Member, seat {}>'.format(self.seat)

