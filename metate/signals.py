# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StoneHandling, Stone, Flange

@receiver(post_save, sender=StoneHandling)
def handle_stone_handling(sender, instance, created, **kwargs):
    if not created:
        return

    hinban_list = {'1235': 'CPR6EA9', '0000': 'NEW',}
    stone = instance.stone
    action = instance.action
    flange = instance.flange
    design_number = instance.design_number
    new_design_number = instance.new_design_number

    if flange and flange.stone and flange.stone != stone:
        raise ValueError("The selected flange is not associated with the selected stone.")
    
    if not flange:
        raise ValueError("Flange must be selected for this action.")

    if action == 'discarded' and stone.main_state in ['WITH_FLANGE', 'WITH_FLANGE_IN_SPINDLE', 'BY_ITSELF']:
        stone.main_state = 'DISCARDED'
        stone.save()
        if flange:
            flange.stone = None
            flange.current_status = 'STORED'
            flange.save()
    elif action == 'mounted' and stone.main_state in ['BY_ITSELF', 'NEW']:
        if stone.main_state == 'NEW':
            stone.name = hinban_list.get(design_number, stone.name)
        stone.main_state = 'WITH_FLANGE_IN_SPINDLE'
        stone.design_number = design_number
        stone.save()
        if flange:
            flange.stone = stone
            flange.current_status = 'IN_USE'
            flange.save()
    elif action == 'shelved_with_flange' and stone.main_state == 'WITH_FLANGE_IN_SPINDLE':
        stone.main_state = 'WITH_FLANGE'
        stone.save()
        if flange:
            flange.current_status = 'IN_USE'
            flange.save()
    elif action == 'shelved_only_stone' and stone.main_state in ['WITH_FLANGE', 'WITH_FLANGE_IN_SPINDLE']:
        stone.main_state = 'BY_ITSELF'
        stone.save()
        if flange:
            flange.stone = None
            flange.current_status = 'STORED'
            flange.save()
    elif action == 'reinstated' and stone.main_state == 'WITH_FLANGE':
        stone.main_state = 'WITH_FLANGE_IN_SPINDLE'
        stone.save()
        if flange:
            flange.current_status = 'IN_USE'
            flange.save()
    elif action == 'removed' and stone.main_state in ['WITH_FLANGE', 'WITH_FLANGE_IN_SPINDLE']:
        stone.main_state = 'BY_ITSELF'
        stone.save()
        if flange:
            flange.stone = None
            flange.current_status = 'STORED'
            flange.save()
    elif action == 'change_design_number':
        if new_design_number:
            stone.design_number = new_design_number
            stone.save()
        else:
            raise ValueError("Design number must be provided for this action.")
    else:
        raise ValueError("Invalid action for the current stone state or missing required information.")
