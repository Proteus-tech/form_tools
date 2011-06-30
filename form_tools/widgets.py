from django.forms.widgets import FileInput
from django.utils.safestring import mark_safe
from django import forms

class InlineWidget(forms.TextInput):
    def __init__(self, attrs=None, render_value=True):
        if not attrs:
            attrs = {}

        attrs['class'] = 'inline'

        super(InlineWidget, self).__init__(attrs)
        self.render_value = render_value

class InlineTextareaWidget(forms.Textarea):
    def __init__(self, attrs=None, render_value=True):
        if not attrs:
            attrs = {}

        attrs['class'] = 'expandable'
        attrs['rows'] = 0

        super(InlineTextareaWidget, self).__init__(attrs)
        self.render_value = render_value

class ImageFileInput(FileInput):
    def __init__(self, attrs=None):
        super(ImageFileInput, self ).__init__(attrs)

    def render(self, *args, **kwargs):
        rendered_string = super(ImageFileInput, self).render(*args, **kwargs)
        file_url = ''
        if self.attrs.get('file_url', None):
            file_url = self.attrs['file_url']
        if file_url:
            current_file_name = file_url.split("/")[-1]
            del_icon = ""
            if self.attrs.get('del_icon' , ''):
                del_icon = 'checked="checked"'
            rendered_string = rendered_string + u'<br/><label>&nbsp;</label>'
            rendered_string = rendered_string + u'<div class="file_sample" >'
            rendered_string = rendered_string + u'<img src="%s" class="thumbnail" />' % ( file_url )
            rendered_string = rendered_string + u'<span style="vertical-align:top;" >'
            rendered_string = rendered_string + u'%s<br/>'  % ( current_file_name )
            rendered_string = rendered_string + u'<input type="checkbox" name="del_icon" %s />Delete' % ( del_icon )
            rendered_string = rendered_string + '</span>'
            rendered_string = rendered_string + u'</div>'

        return mark_safe(rendered_string)

