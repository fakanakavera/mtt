from django.db import models

class Stone(models.Model):
    name = models.CharField(max_length=255)
    size = models.DecimalField(max_digits=5, decimal_places=2)
    design_number = models.IntegerField()  # Adding a design number field
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.size}mm) - Design {self.design_number}"


class Flange(models.Model):
    number = models.CharField(max_length=50, unique=True)
    stone = models.ForeignKey('Stone', on_delete=models.CASCADE, null=True, blank=True)
    current_status = models.CharField(max_length=50, default='stored')  # e.g., "stored", "in_use", "discarded"

    def __str__(self):
        return f"Flange {self.number} ({self.current_status})"


class Inventory(models.Model):
    stone = models.ForeignKey(Stone, on_delete=models.CASCADE)
    count = models.IntegerField(null=True, blank=True, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stone.name}: {self.count} units"

    def update_count(self, delta):
        self.count += delta
        self.save()


class Production(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    stone = models.ForeignKey(Stone, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    production_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stone.name}: {self.quantity} units - {self.status}"


class Requirement(models.Model):
    stone = models.ForeignKey(Stone, on_delete=models.CASCADE)
    required_quantity = models.IntegerField()
    requirement_month = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stone.name}: {self.required_quantity} units required by {self.requirement_month}"


class StoneHandling(models.Model):
    ACTION_CHOICES = [
        ('discarded', 'Discarded'),     # jogada fora
        ('shelved', 'Shelved'),         # guardada no souko
        ('reinstated', 'Reinstated'),   # reinstalada (flange ou pedra)
        ('assigned', 'Assigned'),       # tirada do souko
        ('removed', 'Removed'),         # pedra removida (caso a pedra seja removida do flange, mas não descartada)
        ('design_number_changed', 'Design Number Changed')  # número de design alterado (tofu)
    ]

    stone = models.ForeignKey(Stone, on_delete=models.CASCADE)
    flange = models.ForeignKey(Flange, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    action_date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stone.name}: {self.action} on {self.action_date} (Flange {self.flange.number if self.flange else 'N/A'})"
