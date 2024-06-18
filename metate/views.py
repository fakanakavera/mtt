from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Stone, Flange, StoneHandling

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
    fields = ['stone', 'flange', 'action', 'action_date', 'notes']
    template_name = 'metate/stonehandling_form.html'
    success_url = reverse_lazy('stone_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse_lazy('stone_list')
        return context

class StoneHandlingListView(ListView):
    model = StoneHandling
    template_name = 'metate/stonehandling_list.html'
