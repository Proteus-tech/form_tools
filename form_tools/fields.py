from django.forms import SlugField
from django.forms.fields import ChoiceField, MultipleChoiceField
from django.forms.util import ValidationError
from django.utils.translation import ugettext_lazy as _

from service_api_tools.api_tools.auth_api_functions import get_users
from service_api_tools.url_tools.url_fullpath_generator import UrlGenerator

class AbbreviationField(SlugField):
    default_error_messages = {
        'invalid': _(u'Enter a valid "abbreviation" consisting of letters, numbers,'
                     u" underscores or hyphens."),
        }

    def clean(self, value):
        value = super(SlugField, self).clean(value)
        if len(value) > 5:
            raise ValidationError(
                _('Ensure this value has at most %d characters (it has %d).') % (5, len(value))
            )
        return value

def get_all_users_username_list():
    users = get_users()
    user_choices = [(user['links']['self']['href'],user['username']) for user in users]
    return user_choices

class UsernameField(ChoiceField):

    def __init__(self, *args, **kwargs):
        super(UsernameField, self).__init__(
            *args,
            **kwargs
        )
        self.choices = get_all_users_username_list()

class MultipleUsernameField(MultipleChoiceField):
    """
    supports list of pk or username
    """
    def __init__(self, *args, **kwargs):
        super(MultipleUsernameField, self).__init__(
            *args,
            **kwargs
        )
        self.choices = get_all_users_username_list()

    def validate(self,value):
        if self.required and not value:
            raise ValidationError('This field is required.')
        return super(MultipleUsernameField,self).validate(value)
