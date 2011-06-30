from django.forms.forms import Form

from service_api_tools.http_tools.request import call_service_api

from form_tools import fields as eidos_fields
from form_tools.widgets import ImageFileInput

def import_from_name(name):
    components = name.split('.')
    mod = __import__('.'.join(components[:-1]), globals(), locals(), [components[-1]])
    try:
        klass = getattr(mod, components[-1])
    except AttributeError:
        return None
    return klass

class FormBuilder():
    """
    def get_form_from_builder(project_pk, initial_data={}, data ={}):
        form_builder = FormBuilder('project', '/project/'+ project_pk + '/release/')

        del form_builder.form_dict[ 'created_by' ] #To remove field created_by form the form.
        form_builder.init_form( initial_data , data )

        form_dict = form_builder.form_dict
        for key in form_builder.form_dict.keys():
            this = form_dict[key]['kwargs']
            #Update the widget in form_dict
            form_builder.update_widget( key , extra_attrs={'class':'hello'} )
            #Get the Field
            the_field = form_builder.get_field(
                class_name = form_dict[key]['class'],
                kw = this )
            #Insert the Field to Form
            form_builder.insert_field(key, the_field)

        return form_builder.form
    """
    def __init__(self, form_dict ):
        self.prefix = None
        self.initial = None
        if form_dict.has_key('prefix'):
            self.prefix = form_dict['prefix']
            del form_dict['prefix']
        if form_dict.has_key('initial'):
            self.initial = form_dict['initial']
            del form_dict['initial']
        self.form_dict = form_dict

    def get_widget(self, class_name = "TextInput", extra_attrs={} , widget = None, kw={}):
        """
        Return widget instance.
        """
        kwargs = {}
        for i in kw:
            kwargs[str(i)] = kw[i]
        if not widget:
            from django.forms import widgets
            the_widget = getattr( widgets , class_name )(**kwargs)
        else:
            the_widget = widget(**kwargs)
        the_widget.attrs.update(extra_attrs)
        return the_widget

    def update_widget(self, field_name , extra_attrs = {} , widget=None, kw={}):
        """
        This method will be used when you want to assign widget to the field.
        """
        widget_name = "TextInput"
        if not widget:
            # then we only update the attrs of the current widget
            widget = self.form.fields[field_name].widget
            widget.attrs.update(extra_attrs)
        else:
            self.form.fields[field_name].widget = self.get_widget(  class_name= widget_name , extra_attrs = extra_attrs , widget = widget, kw=kw)


    def get_field(self, class_name = "CharField", kw ={} ):
        # try normal form fields first
        from django.forms import fields as django_fields
        field_class = getattr( django_fields, class_name , None )
        # then try our own customized fields
        if not field_class:
            field_class = getattr( eidos_fields , class_name , None)
        kwargs = {}
        for i in kw:
            kwargs[str(i)] = kw[i]

        if kwargs.get('validators'):
            # the validators were printed into this format <module.class at object 0xxxxxxx> we really need to load the actual class
            validator_list = []
            for name in kwargs['validators']:
                split_name = name.split(' ')
                klass_name = split_name[0]
                klass_name = klass_name.lstrip('<')
                klass = import_from_name(klass_name)
                if klass:
                    validator_list.append(klass)
            kwargs['validators'] = validator_list

        the_field = field_class(**kwargs)
        return the_field

    def init_form(self, initial_data={} , data = {}, ordered_fields=None , *args , **kwargs ):
        if self.initial and not initial_data:
            initial_data = self.initial
        form = Form(data=data or None, initial=initial_data or None, *args ,**kwargs)
        self.form = form

        fields = []
        if ordered_fields:
            fields = ordered_fields
        else:
            fields = self.form_dict.keys()

        for key in fields:
            #turn widget name to widget class
            if not self.form_dict.get(key):
                continue
            widget = self.form_dict[key]['kwargs']['widget']
            widget_name = widget['name']
            widget_kwargs = widget['kwargs']
            if (widget_name == 'Select' or widget_name == 'SelectMultiple') and self.form_dict[key]['kwargs'].has_key('choices'):
                widget_kwargs.update({'choices':self.form_dict[key]['kwargs']['choices']})
            self.form_dict[key]['kwargs']['widget'] = self.get_widget(  class_name= widget_name, kw = widget_kwargs )
            #Get the Field
            the_field = self.get_field(
                class_name = self.form_dict[key]['class'],
                kw = self.form_dict[key]['kwargs'] )
            #Insert the Field to Form
            if self.prefix:
                key = self.prefix + u'-' + key
            self.insert_field(key, the_field)

    def insert_field(self, key , the_field ):
        position = len(self.form.fields)
        self.form.fields.insert( position , key, the_field)
        #print 'self.fields => ', self.form.fields
        #print

def get_prioritized_formset(response_object):
    prioritized_formset = {}
    if response_object and isinstance(response_object,dict) and response_object.has_key('forms'):
        forms = response_object['forms']
        management_form_builder = FormBuilder(response_object['management_form'])
        management_form_builder.init_form()
        prioritized_formset['management_form'] = management_form_builder.form
        prioritized_formset['forms'] = []
        from django.forms.widgets import HiddenInput
        for form_dict in forms:
            form_builder = FormBuilder(form_dict)
            form_builder.init_form()
            for key in form_builder.form.fields:
                if u'-DELETE' not in key:
                    form_builder.update_widget(key,widget=HiddenInput)
            prioritized_form = form_builder.form
            prioritized_formset['forms'].append(prioritized_form)
    if response_object.has_key('errors'):
        prioritized_formset['errors'] = response_object['errors']
    if response_object.has_key('non_form_errors'):
        prioritized_formset['non_form_errors'] = response_object['non_form_errors']
    return prioritized_formset

def get_release_form_from_builder(project_pk, initial_data={}, data ={}):
    url = '/project/'+ project_pk + '/release/'
    status_code, response_object = call_service_api('project', url,'GET')
    form_builder = FormBuilder(response_object)

    del form_builder.form_dict[ 'project' ]

    new_field_order = [ 'name', 'number', 'iteration_length', 'estimated_velocity', 'start_date', 'release_date']

    form_builder.init_form( initial_data=initial_data , data=data , ordered_fields=new_field_order , auto_id=False)

    for key in new_field_order:
        #Update the widget in form_dict
        if key.endswith("_date"):
            form_builder.update_widget( key , extra_attrs={'class':'release_form dateinput'} )
        else:
            form_builder.update_widget( key , extra_attrs={'class':'release_form'} )
    return form_builder.form

#Get Project Form
def get_project_form_from_builder(initial_data={}, data ={} , change_form=False):
    url = '/project/'
    if change_form:
        url = '%s?edit=True' % (url)
    status_code, response_object = call_service_api('project', url,'GET')
    form_builder = FormBuilder(response_object)

    new_field_order = [ 'name', 'description' ,'abbreviation', 'icon',
                       'start_date', 'managers', 'agile_coaches']

    form_builder.init_form( initial_data , data , ordered_fields=new_field_order, auto_id=False)

    for key in new_field_order:
        #Update the widget in form_dict
        if key not in form_builder.form.fields.keys():
            continue
        if key.endswith("_date"):
            form_builder.update_widget( key , extra_attrs={'class':'project_form dateinput'} )
        elif key == 'icon':
            icon_url = ""
            if initial_data.get('icon_url', None):
                icon_url = initial_data['icon_url']
            del_icon = ""
            if initial_data.get('del_icon',None):
                del_icon = initial_data['del_icon']
            form_builder.update_widget( key ,
                                        extra_attrs={
                                            'class':'project_form',
                                            'file_url': icon_url,
                                            'del_icon': del_icon
                                            } ,
                                        widget = ImageFileInput )
        else:
            form_builder.update_widget( key , extra_attrs={'class':'project_form'} )
    return form_builder.form

def get_project_edit_form_from_builder(initial_data={}, data ={}):
    return get_project_form_from_builder(initial_data,data,change_form=True)