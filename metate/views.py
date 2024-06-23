from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Stone, Flange, StoneHandling
from django.contrib import messages

class StoneListView(ListView):
    model = Stone
    template_name = 'metate/stone_list.html'

class StoneDetailView(DetailView):
    model = Stone
    template_name = 'metate/stone_detail.html'

class StoneCreateView(CreateView):
    model = Stone
    fields = ['name', 'size', 'design_number', 'description']
    template_name = 'metate/stone_form.html'
    success_url = reverse_lazy('stone_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('stone_list')
        return context

class StoneUpdateView(UpdateView):
    model = Stone
    fields = ['name', 'size', 'design_number', 'description']
    template_name = 'metate/stone_form.html'
    success_url = reverse_lazy('stone_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('stone_list')
        return context

class StoneDeleteView(DeleteView):
    model = Stone
    template_name = 'metate/stone_confirm_delete.html'
    success_url = reverse_lazy('stone_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('stone_list')
        return context

class FlangeListView(ListView):
    model = Flange
    template_name = 'metate/flange_list.html'

class FlangeCreateView(CreateView):
    model = Flange
    fields = ['number', 'stone', 'current_status']
    template_name = 'metate/flange_form.html'
    success_url = reverse_lazy('flange_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('flange_list')
        return context

class FlangeUpdateView(UpdateView):
    model = Flange
    fields = ['number', 'stone', 'current_status']
    template_name = 'metate/flange_form.html'
    success_url = reverse_lazy('flange_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('flange_list')
        return context

class FlangeDeleteView(DeleteView):
    model = Flange
    template_name = 'metate/flange_confirm_delete.html'
    success_url = reverse_lazy('flange_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('flange_list')
        return context

class StoneHandlingCreateView(CreateView):
    model = StoneHandling
    fields = ['design_number' ,'stone', 'flange', 'action', 'action_date', 'notes']
    template_name = 'metate/stonehandling_form.html'
    success_url = reverse_lazy('stone_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('stone_list')
        return context
    
    def form_valid(self, form):
        stone = form.cleaned_data['stone']
        action = form.cleaned_data['action']
        flange = form.cleaned_data['flange']

        # Check if the selected flange is associated with the selected stone
        if flange:
            print(flange.stone)
            if flange.stone != None and flange.stone != stone:
                form.add_error(None, "The selected flange is not associated with the selected stone.")
                return self.form_invalid(form)

        # Perform additional checks and actions based on the action
        if action == 'discarded' and stone.main_state not in ['DISCARDED']:
            stone.main_state = 'DISCARDED'
            stone.save()
            if flange:
                flange.stone = None
                flange.current_status = 'STORED'
                flange.save()
            StoneHandling.objects.create(stone=stone, action='discarded', action_date=form.cleaned_data['action_date'])

        elif action == 'shelved_with_flange' and stone.main_state == 'WITH_FLANGE_IN_SPINDLE':
            stone.main_state = 'WITH_FLANGE'
            stone.save()
            if flange:
                flange.current_status = 'STORED'
                flange.save()
            StoneHandling.objects.create(stone=stone, action='shelved_with_flange', action_date=form.cleaned_data['action_date'])

        elif action == 'shelved_only_stone' and stone.main_state == 'WITH_FLANGE':
            stone.main_state = 'BY_ITSELF'
            stone.save()
            if flange:
                flange.stone = None
                flange.current_status = 'STORED'
                flange.save()
            StoneHandling.objects.create(stone=stone, action='shelved_only_stone', action_date=form.cleaned_data['action_date'])

        elif action == 'reinstated' and stone.main_state == 'WITH_FLANGE_IN_SPINDLE':
            stone.main_state = 'WITH_FLANGE_IN_SPINDLE'
            stone.save()
            if flange:
                flange.current_status = 'IN_USE'
                flange.save()
            StoneHandling.objects.create(stone=stone, action='reinstated', action_date=form.cleaned_data['action_date'])

        elif action == 'mounted' and stone.main_state == 'BY_ITSELF':
            stone.main_state = 'WITH_FLANGE'
            stone.design_number = form.cleaned_data['design_number']
            stone.save()
            if flange:
                flange.stone = stone
                flange.current_status = 'IN_USE'
                flange.save()
            StoneHandling.objects.create(stone=stone, action='mounted', action_date=form.cleaned_data['action_date'])

        elif action == 'removed' and stone.main_state == 'WITH_FLANGE':
            stone.main_state = 'BY_ITSELF'
            stone.save()
            if flange:
                flange.stone = None
                flange.current_status = 'STORED'
                flange.save()
            StoneHandling.objects.create(stone=stone, action='removed', action_date=form.cleaned_data['action_date'])

        elif action == 'change_design_number':
            new_design_number = self.request.POST.get('new_design_number')
            if new_design_number:
                stone.design_number = new_design_number
                stone.save()
                StoneHandling.objects.create(stone=stone, action='change_design_number', action_date=form.cleaned_data['action_date'])
            else:
                form.add_error(None, "Design number must be provided for this action.")
                return self.form_invalid(form)

        else:
            form.add_error(None, "Invalid action for the current stone state or missing required information.")
            return self.form_invalid(form)

        return super().form_valid(form)

class StoneHandlingListView(ListView):
    model = StoneHandling
    template_name = 'metate/stonehandling_list.html'
