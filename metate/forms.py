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
            # Define your filtering logic here
            if state == 'NEW' or state == 'BY_ITSELF':
                self.fields['action'].choices = [
                    ('mount_flange', 'Mount Flange'),
                    # Add other relevant actions
                ]
            elif state == 'WITH_FLANGE':
                self.fields['action'].choices = [
                    ('remove_flange', 'Remove Flange'),
                    # Add other relevant actions
                ]
            # Add more conditions based on stone states

class StoneHandlingStep3Form(forms.ModelForm):
    class Meta:
        model = StoneHandling
        fields = ['design_number', 'new_design_number', 'action_date', 'notes']
