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
        super(StoneHandlingStep2Form, self).__init__(*args, **kwargs)
        if stone:
            state = stone.main_state
            choices = load_yaml(os.path.join(DIR, 'variables', 'stonehandling_form_step2.yaml'))

            self.fields['action'].choices = choices[state]
        
        if not stone:
            choices = load_yaml(os.path.join(DIR, 'variables', 'stonehandling_form_step2.yaml'))
            self.fields['action'].choices = choices['EMPTY_FLANGE']

class StoneHandlingStep3Form(forms.ModelForm):
    class Meta:
        model = StoneHandling
        fields = ['design_number', 'action_date', 'action']

    def __init__(self, *args, **kwargs):
        selected_action = kwargs.pop('selected_action', None)
        super(StoneHandlingStep3Form, self).__init__(*args, **kwargs)
        print(f"Selected action: {selected_action}")
        choices = load_yaml(os.path.join(DIR, 'variables', 'stonehandling_form_step3.yaml'))
        self.fields['stone'] = forms.ModelChoiceField(queryset=Stone.objects.filter(main_state='NEW'))
        self.fields['action'].choices = selected_action
