from django.forms.util import ErrorList

def export_form_to_json(form_class = None, form_instance = None, model = None ):
    """
    Export Form Instance or Form class to JSON object.
    Set ModelForm if Model given.
    """
    if form_class:
        form = form_class()
        field_list = form.fields.items()
    elif form_instance:
        form = form_instance
        field_list = form.fields.items()

    ignore_attribute_list = [ 'regex', 'creation_counter', 'empty_label' , 'choice_cache','_queryset']
    if field_list:
        result = {}
        if form.prefix:
            result['prefix'] = form.prefix
        if form.initial:
            result['initial'] = form.initial
        for name,val in field_list:
            #print name , " ", val.__class__.__name__
            initial = None
            if form.initial and form.initial.has_key(name):
                initial = form.initial[name]
            if val.__class__.__name__ == 'InlineForeignKeyField' or val.__class__.__name__ == 'ModelChoiceField':
                result[name] = {'class':'Field'}
            else:
                result[name] = {'class':val.__class__.__name__}
            this = result[name]['kwargs'] = {}
            for v in vars(val):
                attr_val = val.__getattribute__(v)

                if v == "widget" :
                    #print "---------", v, " :: ", val.widget.__class__.__name__
                    this[v] = {}
                    if val.widget.__class__.__name__ == 'InlineForeignKeyHiddenInput':
                        this[v]['name'] = 'HiddenInput'
                    else:
                        this[v]['name'] = val.widget.__class__.__name__
                    kwargs = {}
                    kwargs['attrs'] = getattr(val.widget,'attrs',{})
                    if val.widget.__class__.__name__ == 'DateInput':
                        kwargs['format'] = getattr(val.widget,'format',None)
                    this[v]['kwargs'] = kwargs

                elif v == "label" :
                    #print "---------", v, " :: ", val.label #._proxy____unicode_cast()
                    if attr_val:
                        if not isinstance(attr_val,unicode):
                            attr_val = attr_val._proxy____unicode_cast()
                        this[v] = attr_val
                elif v == "error_messages":
                    for ek in attr_val:
                        if not isinstance(attr_val[ek], unicode):
                            attr_val[ek] = attr_val[ek]._proxy____unicode_cast()
                    #print "---------", v, " :: ", attr_val
                    this[v] = attr_val
                elif v in ignore_attribute_list:
                    pass
                elif v == "_choices":
                    if attr_val is None:
                        attr_val = []
                    this['choices'] = attr_val
                ### Added for formset
                elif v == "parent_instance":
                    pass
                elif v == "to_field":
                    pass
                elif v == "pk_field":
                    pass
                ###
                else:
                    this[v] = attr_val
            if val.__class__.__name__ == "UsernameField":
                this['widget']['name'] = "Select"
                del this['show_hidden_initial']
                result[name]['class'] = 'ChoiceField'
            if val.__class__.__name__ == "MultipleUsernameField":
                this['widget']['name'] = "SelectMultiple"
                result[name]['class'] = 'MultipleChoiceField'

            if this.has_key('cache_choices'):
                del this['cache_choices']
            if this.has_key('to_field_name'):
                del this['to_field_name']

            if initial is not None:
                this['initial'] = initial
            this=None

        return result

def export_formset_to_json(formset):
    formset_json = {}
    result_list = []
    for form in formset.forms:
        result_list.append(export_form_to_json(form_instance=form))
    formset_json['forms'] = result_list
    formset_json['management_form'] = export_form_to_json(form_instance=formset.management_form)
    if formset.errors:
        formset_json['errors'] = formset.errors
    if formset.non_form_errors():
        formset_json['non_form_errors'] = formset.non_form_errors()
    return formset_json

def errors_append(form, field_name, message):
    u'''
    Add an ValidationError to a field (instead of __all__) during Form.clean():

    class MyForm(forms.Form):
        def clean(self):
            value_a=self.cleaned_data['value_a']
            value_b=self.cleaned_data['value_b']
            if value_a==... and value_b==...:
                errors_append(self, 'value_a', u'Value A must be ... if value B is ...')
            return self.cleaned_data
    '''
    assert form.fields.has_key(field_name), field_name
    error_list=form.errors.get(field_name)
    if error_list is None:
        error_list=ErrorList()
        form.errors[field_name]=error_list
    error_list.append(message)
