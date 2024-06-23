from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StoneHandling, Inventory

@receiver(post_save, sender=StoneHandling)
def update_inventory(sender, instance, **kwargs):
    if instance.action in ['discarded']:
        # Reduce inventory count
        inventory, created = Inventory.objects.get_or_create(stone=instance.stone)
        inventory.update_count(-1)
    elif instance.action == 'reinstated':
        # Increase inventory count
        inventory, created = Inventory.objects.get_or_create(stone=instance.stone)
        inventory.update_count(1)

@receiver(post_save, sender=StoneHandling)
def handle_stone_action(sender, instance, created, **kwargs):
    if not created:
        return

    action = instance.action

    if action == 'discarded':
        if instance.stone:
            instance.stone.main_state = 'DISCARDED'
            instance.stone.save()
        if instance.flange:
            instance.flange.stone = None
            instance.flange.save()

    elif action == 'shelved_with_flange':
        if instance.stone:
            instance.stone.main_state = 'WITH_FLANGE'
            instance.stone.save()
        if instance.flange:
            instance.flange.current_status = 'STORED'
            instance.flange.save()

    elif action == 'shelved_only_stone':
        if instance.stone:
            instance.stone.main_state = 'BY_ITSELF'
            instance.stone.save()
        if instance.flange:
            instance.flange.stone = None
            instance.flange.current_status = 'STORED'
            instance.flange.save()

    elif action == 'reinstated':
        if instance.flange and instance.stone:
            instance.stone.main_state = 'WITH_FLANGE_IN_SPINDLE'
            instance.stone.save()
            instance.flange.current_status = 'IN_USE'
            instance.flange.save()

    elif action == 'mounted':
        if instance.flange and instance.stone:
            instance.stone.main_state = 'WITH_FLANGE'
            instance.stone.save()
            instance.flange.stone = instance.stone
            instance.flange.current_status = 'IN_USE'
            instance.flange.save()

    elif action == 'removed':
        if instance.stone:
            instance.stone.main_state = 'BY_ITSELF'
            instance.stone.save()
        if instance.flange:
            instance.flange.stone = None
            instance.flange.current_status = 'STORED'
            instance.flange.save()
