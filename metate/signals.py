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
