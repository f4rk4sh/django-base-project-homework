from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView
from .forms import SignupForm
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .tasks import send_verification_email

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


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'authentication/register.html'
    form_class = SignupForm
    success_url = reverse_lazy('authentication:register')
    success_message = 'Please confirm your email address to complete the registration'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()

        current_site = get_current_site(self.request)
        body = {'user': self.object.username,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)),
                'token': account_activation_token.make_token(self.object),
                }
        subject = 'Activate your account'
        message = render_to_string('authentication/acc_active_email.html', body)
        recipient = self.object.email
        send_verification_email.delay(subject, message, recipient)
        return super().form_valid(form)


class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')
