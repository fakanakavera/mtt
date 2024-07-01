from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from .models import Stone, Flange, StoneHandling
from django.shortcuts import redirect, get_object_or_404
from .forms import StoneHandlingStep1Form, StoneHandlingStep2Form, StoneHandlingStep3Form

class StoneHandlingStep1View(FormView):
    template_name = 'metate/stonehandling_step1.html'
    form_class = StoneHandlingStep1Form

    def form_valid(self, form):
        self.request.session['flange'] = form.cleaned_data['flange'].id
        return redirect('stonehandling_step2')

class StoneHandlingStep2View(FormView):
    template_name = 'metate/stonehandling_step2.html'
    form_class = StoneHandlingStep2Form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        flange_id = self.request.session.get('flange')
        if flange_id:
            flange = get_object_or_404(Flange, id=flange_id)
            stone = flange.stone
            kwargs['stone'] = stone
            kwargs['selected_flange'] = flange
        return kwargs

    def form_valid(self, form):
        self.request.session['action'] = form.cleaned_data['action']
        return redirect('stonehandling_step3')

class StoneHandlingStep3View(FormView):
    template_name = 'metate/stonehandling_step3.html'
    form_class = StoneHandlingStep3Form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        flange_id = self.request.session.get('flange')

        selected_action = self.request.session.get('action')
        if selected_action:
            kwargs['selected_action'] = selected_action

        if flange_id:
            flange = get_object_or_404(Flange, id=flange_id)
            kwargs['selected_flange'] = flange
        return kwargs

    def form_valid(self, form):
        # Retrieve data from the session
        action = self.request.session.get('action')
        flange_id = self.request.session.get('flange')
        flange = get_object_or_404(Flange, id=flange_id)
        if flange.stone:
            stone = flange.stone
        else:
            stone = form.cleaned_data['stone']

        if action == 'hanten':
            design_number = stone.design_number
        else:
            design_number = form.cleaned_data['design_number']
        
        print(f"flange: {flange}")
        print(f"stone: {stone}")
        print(f"action: {action}")
        print(f"design_number: {design_number}")
        print(f"new_design_number: {form.cleaned_data.get('new_design_number', None)}")
        print(f"action_date: {form.cleaned_data.get('action_date', None)}")
        print(f"notes: {form.cleaned_data.get('notes', None)}")

        # Create the StoneHandling object
        StoneHandling.objects.create(
            flange=flange,
            action=action,
            stone=stone,
            design_number=form.cleaned_data.get('design_number', None),
            new_design_number=form.cleaned_data.get('new_design_number', None),
            action_date=form.cleaned_data.get('action_date', None),
            notes=form.cleaned_data.get('notes', None),
        )

        # Clear the session data
        self.request.session.pop('flange')
        self.request.session.pop('action')

        return redirect('stone_list')
    

    

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

# class StoneHandlingCreateView(CreateView):
#     model = StoneHandling
#     fields = ['design_number' ,'stone', 'flange', 'action', 'new_design_number', 'action_date', 'notes']
#     template_name = 'metate/stonehandling_form.html'
#     success_url = reverse_lazy('stone_list')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['cancel_url'] = reverse_lazy('stone_list')
#         return context
    
#     def form_valid(self, form):
#         hinban_list = {'1235': 'CPR6EA9',
#                        '0000': 'NEW',}
#         stone = form.cleaned_data['stone']
#         action = form.cleaned_data['action']
#         flange = form.cleaned_data['flange']
#         design_number = form.cleaned_data['design_number']
#         new_design_number = form.cleaned_data['new_design_number']

#         # Check if the selected flange is associated with the selected stone
#         if flange:
#             if flange.stone != None and flange.stone != stone:
#                 form.add_error(None, "The selected flange is not associated with the selected stone.")
#                 return self.form_invalid(form)
#         else:
#             form.add_error(None, "Flange must be selected for this action.")
#             return self.form_invalid(form)

#         # JOGA A PEDRA FORA
#         if action == 'discarded' and stone.main_state in ['WITH_FLANGE', 'WITH_FLANGE_IN_SPINDLE', 'BY_ITSELF']:
#             stone.main_state = 'DISCARDED'
#             stone.save()
#             if flange:
#                 flange.stone = None
#                 flange.current_status = 'STORED'
#                 flange.save()
#         # MONTA UM PEDRA NO FLANGE
#         elif action == 'mounted' and stone.main_state in ['BY_ITSELF', 'NEW']:
#             if stone.main_state == 'NEW':
#                 stone.name = hinban_list[design_number]
#             stone.main_state = 'WITH_FLANGE_IN_SPINDLE'
#             stone.design_number = design_number
#             stone.save()
#             if flange:
#                 flange.stone = stone
#                 flange.current_status = 'IN_USE'
#                 flange.save()
#         # GUARDA PEDRA COM FLANGE
#         elif action == 'shelved_with_flange' and stone.main_state in ['WITH_FLANGE_IN_SPINDLE']:
#             stone.main_state = 'WITH_FLANGE'
#             stone.save()
#             if flange:
#                 flange.current_status = 'IN_USE'
#                 flange.save()
#         # GUARDA PEDRA SEM FLANGE
#         elif action == 'shelved_only_stone' and stone.main_state in ['WITH_FLANGE', 'WITH_FLANGE_IN_SPINDLE']:
#             stone.main_state = 'BY_ITSELF'
#             stone.save()
#             if flange:
#                 flange.stone = None
#                 flange.current_status = 'STORED'
#                 flange.save()
#         # REINSTALA FLANGE
#         elif action == 'reinstated' and stone.main_state in ['WITH_FLANGE']:
#             stone.main_state = 'WITH_FLANGE_IN_SPINDLE'
#             stone.save()
#             if flange:
#                 flange.current_status = 'IN_USE'
#                 flange.save()
#         # REMOVE PEDRA DO FLANGE
#         elif action == 'removed' and stone.main_state in ['WITH_FLANGE', 'WITH_FLANGE_IN_SPINDLE']:
#             stone.main_state = 'BY_ITSELF'
#             stone.save()
#             if flange:
#                 flange.stone = None
#                 flange.current_status = 'STORED'
#                 flange.save()
#         # ALTERA NUMERO DO DESIGN
#         elif action == 'change_design_number':
#             if new_design_number:
#                 stone.design_number = new_design_number
#                 stone.save()
#             else:
#                 form.add_error(None, "Design number must be provided for this action.")
#                 return self.form_invalid(form)

#         else:
#             form.add_error(None, "Invalid action for the current stone state or missing required information.")
#             return self.form_invalid(form)
        

#         return super().form_valid(form)

class StoneHandlingListView(ListView):
    model = StoneHandling
    template_name = 'metate/stonehandling_list.html'
