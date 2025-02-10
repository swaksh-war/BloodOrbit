from django.shortcuts import render, redirect
from .models import Donor
from django.http import HttpResponse
from .utils import get_compatible_donors
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib.auth.decorators import login_required

def home(request):
    print((request.user))
    return render(request, 'home.html')


def register_donor(request):
    if request.method == 'POST':
        name = request.POST['name']
        blood_group = request.POST['blood_group']
        age = request.POST['age']
        long_term_disease = request.POST['long_term_disease']
        last_time_donated = request.POST['last_time_donated']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        contact_number = request.POST['contact_number']
        donor = Donor(name=name, blood_group=blood_group, age=age, long_term_disease=long_term_disease, last_time_donated=last_time_donated ,latitude=latitude, longitude=longitude, contact_number=contact_number)
        donor.save()
        return HttpResponse("New Donor Registered")
    return render(request, 'donor_register.html')

def search_donors(request):
    if request.method == 'POST':
        blood_group = request.POST['blood_group']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        compatible_donor = get_compatible_donors(float(latitude), float(longitude), blood_group)
        context = {
            'donors' : compatible_donor
        }
        return render(request, 'search_donor.html', context)
    return render(request, 'search_donor.html')

 
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return redirect('home')
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Invalid credentials")
    return render(request, 'home.html')

def user_logout(request):
    logout(request)
    return redirect('home')


@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        user = request.user
        username = user.username
        recipient_email = request.POST.get('recipient_email')
        if not recipient_email:
            return HttpResponse("Recipient email is missing.", status=400)
        
        FROM_EMAIL = "bloodorbit5@gmail.com"
        FROM_EMAIL_PASSWORD = "xsqpavobvrkrkyuo"
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = 'Blood Donation Request'
        message = f'We request you to donate blood to save a life. Please contact the requester {username} for further details.'
        msg.attach(MIMEText(message, 'plain'))
        
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(FROM_EMAIL, FROM_EMAIL_PASSWORD)
                server.sendmail(FROM_EMAIL, recipient_email, msg.as_string())
            return HttpResponse("Email sent successfully.")
        except Exception as e:
            return HttpResponse(f"Error sending email: {e}", status=500)
    return HttpResponse("Invalid request method.", status=405)


@csrf_exempt
def send_message_twilio(request):
    if request.method=='POST':
        user = request.user
        username = user.username
        mobile_number = request.POST.get('mobile_number')
        senders_number = request.POST.get('recipient_number')
        if not senders_number:
            return HttpResponse("Recipient number is missing.", status=400)
        from twilio.rest import Client
        import configparser
        config = configparser.ConfigParser()
        config.read('creds.conf')
        account_sid = config.get('twilio', 'ACCOUNT_SID')
        auth_token = config.get('twilio', 'AUTH_TOKEN')
        twilio_number = config.get('twilio', 'TWILIO_NUMBER')
        client = Client(account_sid, auth_token)
        number = "+91" + str(senders_number)
        message = client.messages.create(
            body=f'Urgent! we need blood donation. Please contact the requester {username} for further details in this number {mobile_number}',
            from_=twilio_number,
            to=number
        )
        # print(mobile_nuber, senders_number, username)
    return HttpResponse("Message sent Successfully.", status=200)
