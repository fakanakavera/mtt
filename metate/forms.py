from django import forms
from .models import StoneHandling, Stone
from fnkutils.funcs.yaml import load_yaml
import os

DIR = os.path.dirname(os.path.abspath(__file__))

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
        self.fields['selected_flange'].widget.attrs['readonly'] = True
        self.fields['selected_flange'].initial = flange
        if stone:
            state = stone.main_state
            self.fields['action'].choices = choices[state]
        
        if not stone:
            self.fields['action'].choices = choices['EMPTY_FLANGE']

class StoneHandlingStep3Form(forms.ModelForm):
    class Meta:
        model = StoneHandling
        fields = ['design_number', 'action_date']

    def __init__(self, *args, **kwargs):
        selected_action = kwargs.pop('selected_action', None)
        super(StoneHandlingStep3Form, self).__init__(*args, **kwargs)
        self.fields['stone'] = forms.ModelChoiceField(queryset=Stone.objects.filter(main_state='NEW'))

