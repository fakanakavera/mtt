from django import forms
from .models import StoneHandling, Stone
from fnkutils.funcs.yaml import load_yaml
import os

DIR = os.path.dirname(os.path.abspath(__file__))

def _initialize_custom_field(self, field_name, label, required=False, readonly=True, disabled=False, initial=None):
    self.fields[field_name] = forms.CharField(label=label, required=required)
    self.fields[field_name].widget.attrs['readonly'] = readonly
    self.fields[field_name].widget.attrs['disabled'] = disabled
    self.fields[field_name].initial = initial

def _initialize_selected_action_field(self, selected_action):
    _initialize_custom_field(self, 
                            'selected_action', 
                            'Selected Action', 
                            required=False, 
                            readonly=True, 
                            disabled=True, 
                            initial=selected_action
                        )

def _initialize_selected_flange_field(self, selected_flange):
    _initialize_custom_field(self, 
                            'selected_flange', 
                            'Selected Flange', 
                            required=False, 
                            readonly=True, 
                            disabled=True, 
                            initial=selected_flange
                        )

class StoneHandlingStep1Form(forms.ModelForm):
    class Meta:
        model = StoneHandling
        fields = ['flange']

class StoneHandlingStep2Form(forms.ModelForm):
    class Meta:
        model = StoneHandling
        fields = ['action']

    def __init__(self, *args, **kwargs):
        stone = kwargs.pop('stone', None)
        flange = kwargs.pop('selected_flange', None)
        super(StoneHandlingStep2Form, self).__init__(*args, **kwargs)
        choices = load_yaml(os.path.join(DIR, 'variables', 'stonehandling_form_step2.yaml'))
        _initialize_selected_flange_field(self, flange)

        # if flange has a stone
        if stone:
            state = stone.main_state
            self.fields['action'].choices = choices[state]
        # if flange has no stone
        if not stone:
            self.fields['action'].choices = choices['EMPTY_FLANGE']
        

class StoneHandlingStep3Form(forms.ModelForm):
    class Meta:
        model = StoneHandling
        fields = ['design_number', 'action_date']

    def __init__(self, *args, **kwargs):
        selected_action = kwargs.pop('selected_action', None)
        selected_flange = kwargs.pop('selected_flange', None)
        super(StoneHandlingStep3Form, self).__init__(*args, **kwargs)

        _initialize_selected_flange_field(self, selected_flange)
        _initialize_selected_action_field(self, selected_action)

        self.fields['stone'] = forms.ModelChoiceField(queryset=Stone.objects.filter(main_state='NEW'))

