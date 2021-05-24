from django.shortcuts import render
from django.contrib.auth import logout,login,authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import login
from .forms import NewUserForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .token_generator import account_activation_token
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate your account'
            message = render_to_string('users/activate.html',{
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            to_email = form.cleaned_data.get("email")
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponseRedirect(reverse('index'))

    else:
        form = NewUserForm()
    context = {'form': form} 
    return render(request,"users/register.html", context)  

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()    
        login(request, user)
        return HttpResponseRedirect(reverse('users:success'))
    else:
        return HttpResponse('Token is invalid!')    

