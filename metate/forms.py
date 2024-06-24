from django import forms
from .models import StoneHandling, Stone

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
            action_choices = []
            if state in ['NEW', 'BY_ITSELF']:
                action_choices = [
                    ('mount_flange', 'Mount Flange'),
                    # Add other relevant actions for this state
                ]
            elif state == 'WITH_FLANGE':
                action_choices = [
                    ('remove_flange', 'Remove Flange'),
                    ('discard', 'Discard'),
                    # Add other relevant actions for this state
                ]
            # Update the action field choices
            self.fields['action'].choices = action_choices

class StoneHandlingStep3Form(forms.ModelForm):
    class Meta:
        model = StoneHandling
        fields = ['design_number', 'new_design_number', 'action_date', 'notes']
