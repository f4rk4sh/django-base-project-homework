from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from apps.authentication.forms import UserCreateForm
from django.shortcuts import redirect
from django.http import Http404

UserModel = get_user_model()


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = UserModel.objects.get(username=self.request.user)
        return context


class UserListView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = UserModel.objects.all()
        return context


class RegisterView(FormView):
    template_name = 'authentication/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('authentication:user')

    def form_valid(self, form):
        email = form.data.get('email')
        send_registration_mail.delay(email)
        return super().form_valid(form)


def home(request):
    return reverse_lazy('authentication:user')


def verify(request, uuid):
    try:
        user = UserModel.objects.get(verification_uuid=uuid, is_active=False)
    except UserModel.DoesNotExist:
        raise Http404("User does not exist or is already verified")

    user.is_active = True
    user.save()

    return redirect('home')
