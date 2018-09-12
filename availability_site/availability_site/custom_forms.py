from django import forms
from django.forms.utils import from_current_timezone, to_current_timezone

class MaterialSelect(forms.Select):
    template_name = 'django/forms/widgets/select_material.html'
    option_template_name = 'django/forms/widgets/select_option_material.html'

class MaterialDateInput(forms.DateInput):
    format_key = 'DATE_INPUT_FORMATS'
    template_name = 'django/forms/widgets/date_material.html'


class MaterialDateTimeInput(forms.DateTimeInput):
    format_key = 'DATETIME_INPUT_FORMATS'
    template_name = 'django/forms/widgets/datetime.html'


class MaterialTimeInput(forms.TimeInput):
    format_key = 'TIME_INPUT_FORMATS'
    template_name = 'django/forms/widgets/time_material.html'

class MaterialSelect(forms.Select):
    template_name = 'django/forms/widgets/select_material.html'
    option_template_name = 'django/forms/widgets/select_option_material.html'

class MaterialSplitDateTimeWidget(forms.MultiWidget):
    """
        A widget that splits datetime input into two <input type="text"> boxes.
        """
    supports_microseconds = False
    template_name = 'django/forms/widgets/splitdatetime.html'

    def __init__(self, attrs=None, date_format=None, time_format=None, date_attrs=None, time_attrs=None):
        widgets = (
            MaterialDateInput(
                attrs=attrs if date_attrs is None else date_attrs,
                format=date_format,
            ),
            MaterialTimeInput(
                attrs=attrs if time_attrs is None else time_attrs,
                format=time_format,
            ),
        )
        super().__init__(widgets)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time()]
        return [None, None]