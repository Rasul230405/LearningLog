from django.shortcuts import render
from django.contrib.auth import logout,login,authenticate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login
from .forms import NewUserForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.views.generic import TemplateView

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method != 'POST':
        form = NewUserForm
    else:
        form = NewUserForm(data=request.POST)  
        if form.is_valid():
            new_user = form.save()
            email = request.POST.get("email")
            new_user.is_active = False
            current_site = get_current_site(request)
            email_subject = 'Activate your account'
            message = render_to_string('users/activate.html',
            {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': generate_token.make_token(new_user),
            })

            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                ['resulinci999@gmail.com'],
            )

            email_message.send() 

    context = {'form': form} 
    return render(request,"users/register.html",context)           


class ActivateAccountView(TemplateView):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.INFO, 'account activate succesfully!')
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'users/activate_fail.html', status=401)    
