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
            # action_choices = choices[state]
            # if state in ['NEW', 'BY_ITSELF']:
            #     action_choices = [
            #         ('mount_flange', 'Mount Flange'),
            #         # Add other relevant actions for this state
            #     ]
            # elif state == 'WITH_FLANGE':
            #     action_choices = [
            #         ('removed', 'Removed'),
            #         ('discarded', 'Discarded'),
            #         # Add other relevant actions for this state
            #     ]
            # Update the action field choices
            self.fields['action'].choices = choices[state]
            print(f"Action choices for state {state}: {self.fields['action'].choices}")
        
        if not stone:
            print("No stone provided.")

class StoneHandlingStep3Form(forms.ModelForm):
    class Meta:
        model = StoneHandling
        fields = ['design_number', 'new_design_number', 'action_date', 'notes']
