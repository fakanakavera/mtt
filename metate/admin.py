from django.contrib import admin
from .models import Stone, Inventory, Production, Requirement, StoneHandling

admin.site.register(Stone)
admin.site.register(Inventory)
admin.site.register(Production)
admin.site.register(Requirement)
admin.site.register(StoneHandling)