from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import CreateView
from accounts.forms import RegistrationForm
from accounts.models import Account
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterView(CreateView):
    template_name = "accounts/register.html"
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ["first_name", "last_name",
              "date_of_birth", "bio", "avatar", "sex"]
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
