# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

def datefield_callback(field):
    if isinstance(field, models.DateField):
        field = field.formfield()
        field.input_formats = settings.DATE_INPUT_FORMATS
        invalid_error_message = _('Enter a valid date. The format is MMM DD, YYYY.')
        field.error_messages['invalid'] = invalid_error_message
        return field
    else:
        return field.formfield()