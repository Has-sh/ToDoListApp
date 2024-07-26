import uuid
from django import forms
from .models import *
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

# Create your class/function here.
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter user name'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def activate(request,uidb64,token):
    User=get_user_model()
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except:
        user=None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request,'Activation link is invalid')

    return redirect('login')

def send_activation_email(request,user,to_email):
    mail_subject='Activate your user account.'
    message=render_to_string("activation.html",{
        'user':user.username,
        'domain':get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email=EmailMessage(mail_subject,message,to=[to_email])
    if email.send():
        newMessage=mark_safe(f"Dear <b>{user}</b>, please go to your email's inbox at <b>{to_email}</b> and click on the received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.")
        messages.success(request, newMessage)
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly')

class CaptchaForm(forms.Form):
        captcha=ReCaptchaField(widget=ReCaptchaV2Checkbox)

# Create your views here.
@login_required
def home(request): 
    """
    View for the home page.

    If the request method is POST, it processes the form data and creates a new Note
    based on the form input. If the CAPTCHA is not valid, an error message is shown.
    If the form is valid, a success message is shown.

    If the request method is GET, it renders the home.html template with the CAPTCHA form.

    Args:
        request (HttpRequest): The request object representing the HTTP request.

    Returns:
        HttpResponse: The response object representing the HTTP response.
    """
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        captcha_form=CaptchaForm(request.POST) 
       
        if not captcha_form.is_valid():
            messages.error(request, 'Invalid captcha. Please try again.')
        else:
            new_note = Note(title=title, data=description, due_date=due_date, userId=request.user)
            new_note.save()
            messages.success(request, 'Note added!')
    else:
        captcha_form=CaptchaForm()
    today_date = timezone.now().date()
    return render(request, 'home.html', {'captcha_form': captcha_form, 'today_date': today_date})

def login_user(request):
    """
    View for user login.

    If the request method is POST, it attempts to authenticate the user based on the
    provided username and password. If successful, the user is logged in and redirected
    to the home page. If unsuccessful, an error message is shown.

    If the request method is GET, it renders the login.html template.

    Args:
        request (HttpRequest): The request object representing the HTTP request.

    Returns:
        HttpResponse: The response object representing the HTTP response.
    """
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')
        user = authenticate(request,username=username,password=password)
        if  user is not None:
            login(request,user)
            
            if not remember_me:
                request.session.set_expiry(0)  
            else:
                request.session.set_expiry(60 * 60 * 24 * 7)  
            
            if 'shared_note_token' in request.session:
                token = request.session.pop('shared_note_token')
                return redirect('view_shared_note', token=token)
            
            return redirect('home')
        else:
            messages.error(request,"Invalid credentials. Please check your username and password.")
            return redirect('login')
        
    else:
        return render(request,'login.html')
    
def logout_user(request):
    """
    View for user logout.

    Logs out the currently logged-in user and shows a logout message.

    Args:
        request (HttpRequest): The request object representing the HTTP request.

    Returns:
        HttpResponse: The response object representing the HTTP response.
    """
    logout(request)
    messages.error(request, 'You Were Logged Out')
    return redirect('login')

def signup(request):
    """
    View for user registration.

    If the request method is POST, it processes the registration form data, creates a new
    user with the provided information, and sends an activation email to the user.
    If the form is valid, the user is redirected to the login page.

    If the request method is GET, it renders the signup.html template with the registration form.

    Args:
        request (HttpRequest): The request object representing the HTTP request.

    Returns:
        HttpResponse: The response object representing the HTTP response.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            send_activation_email(request,user,form.cleaned_data.get('email'))

            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

def delete_note(request, note_id):
    """
    View to delete a user's note.

    If the request method is POST, it attempts to delete the note with the given note_id,
    belonging to the currently logged-in user. If the note is found and deleted, the user
    is redirected to the home page. If the note is not found, a JSON response with an error
    message and status code 404 is returned. If the request method is not POST, a JSON
    response with an error message and status code 400 is returned.

    Args:
        request (HttpRequest): The request object representing the HTTP request.
        note_id (int): The ID of the note to be deleted.

    Returns:
        HttpResponse: The response object representing the HTTP response.
    """
    if request.method == 'POST':
        try:
            note = Note.objects.get(pk=note_id, userId=request.user)
            note.delete()
            return redirect('home')
        except Note.DoesNotExist:
            return JsonResponse({'error': 'Note not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid method.'}, status=400)

def share_note(request, note_id):
    
    try:
        note = Note.objects.get(pk=note_id, userId=request.user)
        token = str(uuid.uuid4())
        shared_note = SharedNote.objects.create(note=note, token=token)
        share_url = request.build_absolute_uri(reverse('view_shared_note', args=[shared_note.token]))
        newMessage=mark_safe(f'Note shared! Share this <a href="{share_url}">{share_url}</a> with others.')
        messages.success(request, newMessage)
    except Note.DoesNotExist:
        messages.error(request, 'Note not found.')
    return redirect('home')

def view_shared_note(request, token):
    
    if not request.user.is_authenticated:
        request.session['shared_note_token'] = token
        messages.error(request, 'You must have an account to access this shared note.')
        return redirect('login')

    try:
        shared_note = SharedNote.objects.get(token=token)
        note = shared_note.note
        existing_task = Note.objects.filter(userId=request.user, title=note.title).exists()
        if not existing_task:
            new_note = Note.objects.create(
                data=note.data,
                date=timezone.now(),
                userId=request.user,
                title=note.title,
                due_date=note.due_date,
                shared=True,
            )
            messages.success(request, 'Task assigned! You now have your own copy of the shared task.')
        else:
            messages.warning(request, 'Task already exists. You already have your own copy of the shared task.')

        return redirect('home')
    
    except SharedNote.DoesNotExist:
        messages.error(request, 'Invalid shared note.')
        return redirect('login')

def homepage(request):
    return render(request, 'intro.html')
