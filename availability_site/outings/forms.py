from django.forms import inlineformset_factory, ModelForm
from django import forms
from outings.models import Event
from users.models import MyUser
from datetime import datetime


class SplitHalfHiddenDateTimeWidget(forms.SplitDateTimeWidget):
    template_name = 'django/forms/widgets/splithiddendatetime.html'

    def __init__(self, attrs=None, date_format=None, time_format=None, date_attrs=None, time_attrs=None):
        super().__init__(attrs, date_format, time_format, date_attrs, time_attrs)
        self.widgets[0].input_type = 'hidden'


class EventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.date = kwargs.pop('date')
        super(EventForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Event
        fields = ['start_time','end_time']


    start_time = forms.SplitDateTimeField(widget=SplitHalfHiddenDateTimeWidget())
    end_time = forms.SplitDateTimeField(widget=SplitHalfHiddenDateTimeWidget())






BaseBookFormSet = inlineformset_factory(MyUser, Event, form=EventForm)

class BookFormSet(BaseBookFormSet):
    def __init__(self, *args, **kwargs):
        self.date = kwargs.pop('date')
        super(BookFormSet, self).__init__(*args, **kwargs)
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
        return super(BookFormSet, self)._construct_form(*args, **kwargs)