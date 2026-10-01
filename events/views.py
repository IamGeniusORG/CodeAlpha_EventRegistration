from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from .models import Event, Registration
from .forms import UserRegisterForm

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    ordering = ['date']

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_registered'] = Registration.objects.filter(event=self.object, user=self.request.user).exists()
        return context

def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('event_list')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def register_event(request, pk):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=pk)
        
        if event.is_full():
            messages.error(request, 'This event is currently full.')
            return redirect('event_detail', pk=pk)
        
        if Registration.objects.filter(user=request.user, event=event).exists():
            messages.warning(request, 'You are already registered for this event.')
            return redirect('event_detail', pk=pk)
            
        Registration.objects.create(user=request.user, event=event)
        messages.success(request, f'Successfully registered for {event.title}!')
        return redirect('dashboard')
    
    return redirect('event_list')

@login_required
def cancel_registration(request, pk):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=pk)
        registration = Registration.objects.filter(user=request.user, event=event).first()
        if registration:
            registration.delete()
            messages.success(request, f'Successfully cancelled registration for {event.title}.')
        else:
            messages.error(request, 'You are not registered for this event.')
        return redirect('dashboard')
    
    return redirect('event_list')

@login_required
def dashboard(request):
    registrations = Registration.objects.filter(user=request.user).select_related('event').order_by('event__date')
    return render(request, 'users/dashboard.html', {'registrations': registrations})
