from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from .forms import UserCreateForm

User = get_user_model()


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(username=self.request.user)
        return context


class UserListView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class RegisterView(FormView):
    template_name = 'authentication/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('authentication:user')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
