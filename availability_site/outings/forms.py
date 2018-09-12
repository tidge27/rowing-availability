from django.forms import inlineformset_factory, ModelForm
from django import forms
from outings.models import Event, Outing, OutingMember
from users.models import MyUser
from datetime import datetime
from availability_site.custom_forms import MaterialSplitDateTimeWidget, MaterialSelect
from groups.models import Group


class SplitHalfHiddenDateTimeWidget(forms.SplitDateTimeWidget):
    template_name = 'django/forms/widgets/splithiddendatetime.html'

    def __init__(self, attrs=None, date_format=None, time_format=None, date_attrs=None, time_attrs=None):
        super().__init__(attrs, date_format, time_format, date_attrs, time_attrs)
        self.widgets[0].input_type = 'hidden'


class EventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.date = kwargs.pop('date')
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].initial = self.date
        self.fields['end_time'].initial = self.date

    class Meta:
        model = Event
        fields = ['start_time','end_time']


    start_time = forms.SplitDateTimeField(widget=SplitHalfHiddenDateTimeWidget(time_attrs={"type":"time"}))
    end_time = forms.SplitDateTimeField(widget=SplitHalfHiddenDateTimeWidget(time_attrs={"type":"time"}))


BaseEventFormSet = inlineformset_factory(MyUser, Event, form=EventForm)

class EventFormSet(BaseEventFormSet):
    def __init__(self, *args, **kwargs):
        self.date = kwargs.pop('date')
        super(EventFormSet, self).__init__(*args, **kwargs)
    def clean(self):
        super().clean()

        for form in self.forms:
            pass
            # name = form.cleaned_data['name'].upper()
            # form.cleaned_data['name'] = name
            # # update the instance value.
            # form.instance.name = name
    def _construct_form(self, *args, **kwargs):
        kwargs['date'] = self.date
        return super(EventFormSet, self)._construct_form(*args, **kwargs)


class OutingMemberForm(ModelForm):

    class Meta:
        model = OutingMember
        fields = ['seat', 'user']

BaseGroupMemberFormSet = inlineformset_factory(Outing, OutingMember, form=OutingMemberForm, extra=10, max_num=9)

class OutingMemberFormSet(BaseGroupMemberFormSet):
    def __init__(self, *args, **kwargs):
        super(OutingMemberFormSet, self).__init__(*args, **kwargs)
        self.queryset = self.queryset.order_by('-seat')


class OutingModelForm(ModelForm):
    start_time = forms.SplitDateTimeField(widget=MaterialSplitDateTimeWidget(
        time_attrs={"type": "time", "label":"Start Time", "container_style":"margin:8px 0px; width:calc(50% - 8px)"},
        date_attrs={"type": "date", "label":"Start Date", "container_style":"margin:8px 0px; width:calc(50% - 8px); margin-right:16px;"}
    ))
    end_time = forms.SplitDateTimeField(widget=MaterialSplitDateTimeWidget(
        time_attrs={"type": "time","label":"End Time", "container_style":"margin:8px 0px; width:calc(50% - 8px)"},
        date_attrs={"type": "date","label":"End Date", "container_style":"margin:8px 0px; width:calc(50% - 8px); margin-right:16px;"}
    ))
    group = forms.ModelChoiceField(widget=MaterialSelect(attrs={"container_style":"margin:8px 0px; width:100%","label":"Group"}), queryset=Group.objects.all())



    class Meta:
        model = Outing
        fields = ['start_time', 'end_time', 'group']
        labels = {
            "group": "WOOP GROOP",
        }