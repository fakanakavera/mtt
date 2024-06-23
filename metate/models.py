from django.db import models

class Stone(models.Model):
    STATE_CHOICES = [
        ('BY_ITSELF', 'By Itself'),
        ('WITH_FLANGE', 'With Flange'),
        ('WITH_FLANGE_IN_SPINDLE', 'With Flange in Spindle'),
        ('NEW', 'New'),
        ('DISCARDED', 'Discarded'),
    ]

    name = models.CharField(max_length=255)
    size = models.DecimalField(max_digits=5, decimal_places=2)
    design_number = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    main_state = models.CharField(max_length=50, choices=STATE_CHOICES, default='NEW')

    def __str__(self):
        return f"{self.name} ({self.size}mm) - Design {self.design_number}"

class Flange(models.Model):
    STATUS_CHOICES = [
        ('STORED', 'Stored'),
        ('IN_USE', 'In Use'),
        ('DISCARDED', 'Discarded'),
    ]

    number = models.CharField(max_length=50, unique=True)
    stone = models.ForeignKey('Stone', on_delete=models.CASCADE, null=True, blank=True)
    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='STORED')

    def __str__(self):
        return f"Flange {self.number} ({self.current_status})"

class Inventory(models.Model):
    stone = models.ForeignKey(Stone, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
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
        ('discarded', 'Discarded'), # stone is discarded
        ('shelved_with_flange', 'Shelved with Flange'), # stone is shelved with a flange
        ('shelved_only_stone', 'Shelved Only Stone'), # stone is shelved without a flange
        ('reinstated', 'Reinstated'), # stone is reinstated on spindle
        ('mounted', 'Mounted'),  # Action for mounting a flange to a stone
        ('removed', 'Removed'),    # Action for removing a flange from a stone
        ('design_number_changed', 'Design Number Changed')  # New action for changing the stone's design number
    ]

    stone = models.ForeignKey(Stone, on_delete=models.CASCADE)
    design_number = models.CharField(max_length=50, null=True, blank=True)
    flange = models.ForeignKey(Flange, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    action_date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stone.name}: {self.action} on {self.action_date} (Flange {self.flange.number if self.flange else 'N/A'})"

class StoneState(models.Model):
    MAIN_STATE_CHOICES = [
        ('BY_ITSELF', 'By Itself'),
        ('WITH_FLANGE', 'With Flange'),
        ('WITH_FLANGE_IN_SPINDLE', 'With Flange in Spindle'),
    ]

    SUB_STATE_CHOICES = [
        ('DONE', 'Done'),
        ('USED', 'Used'),
        ('SEMI_USED', 'Semi-Used'),
        ('TO_BE_DISCARDED', 'To Be Discarded'),
    ]

    stone = models.ForeignKey(Stone, on_delete=models.CASCADE)
    flange = models.ForeignKey(Flange, on_delete=models.CASCADE, null=True, blank=True)
    main_state = models.CharField(max_length=50, choices=MAIN_STATE_CHOICES)
    sub_state = models.CharField(max_length=50, choices=SUB_STATE_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stone.name}: {self.main_state} - {self.sub_state if self.sub_state else 'N/A'}"
