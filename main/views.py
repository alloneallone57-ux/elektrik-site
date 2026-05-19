from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ServiceRequest, Material, StaffStatus, Master, ServicePrice, Review, SEOMeta
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from .telegram_utils import send_to_admin, send_status_update
from .models import TelegramUser

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname', '')
        phone = request.POST.get('phone')
        additional_phone = request.POST.get('additional_phone', '')
        region = request.POST.get('region', '')
        district = request.POST.get('district', '')
        mahalla = request.POST.get('mahalla', '')
        street = request.POST.get('street', '')
        house_number = request.POST.get('house_number', '')
        user_identity = request.POST.get('user_identity', 'Jismoniy shaxs')
        service_type = request.POST.get('service_type', 'Boshqa')
        urgency = request.POST.get('urgency', 'LOW')
        message_text = request.POST.get('message', 'Yo\'q')
        preferred_time = request.POST.get('preferred_time', 'Noma\'lum')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')

        if name and phone:
            image = request.FILES.get('image')
            # Bazaga saqlash
            ServiceRequest.objects.create(
                name=name,
                surname=surname,
                phone=phone,
                additional_phone=additional_phone,
                region=region,
                district=district,
                mahalla=mahalla,
                street=street,
                house_number=house_number,
                user_identity=user_identity,
                service_type=service_type,
                urgency=urgency,
                message=message_text,
                preferred_time=preferred_time,
                image=image,
                latitude=lat if lat else None,
                longitude=lon if lon else None
            )
            
            # Telegramga yuborish
            send_to_admin(
                name=name, surname=surname, phone=phone, region=region,
                user_identity=user_identity, service=service_type, message=message_text,
                preferred_time=preferred_time, additional_phone=additional_phone,
                district=district, mahalla=mahalla, street=street, house_number=house_number,
                urgency=urgency
            )
            
            messages.success(request, "Murojaatingiz qabul qilindi!")
            return redirect('materials_view', service_type=service_type)
    
    masters = Master.objects.filter(is_active=True)
    prices = ServicePrice.objects.all()
    
    return render(request, 'main/index.html', {
        'masters': masters,
        'prices': prices
    })

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('worker_dashboard')
        else:
            messages.error(request, "Login yoki parol xato!")
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def materials_view(request, service_type):
    materials = Material.objects.filter(service_name__icontains=service_type).first()
    return render(request, 'main/materials.html', {'materials': materials, 'service_type': service_type})

@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('worker_dashboard')
    # Statistika ma'lumotlari
    total_requests = ServiceRequest.objects.count()
    new_requests = ServiceRequest.objects.filter(status='NEW').count()
    staff = StaffStatus.objects.first()
    recent_requests = ServiceRequest.objects.all().order_by('-created_at')[:20]
    materials = Material.objects.all()
    
    # Chart data: Status distribution
    status_counts = list(ServiceRequest.objects.values('status').annotate(count=Count('id')))
    
    # Chart data: Region distribution
    region_counts = list(ServiceRequest.objects.values('region').annotate(count=Count('id')))
    
    # Chart data: Last 7 days activity
    today = timezone.now().date()
    activity_labels = []
    activity_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        activity_labels.append(d.strftime('%d.%m'))
        activity_data.append(ServiceRequest.objects.filter(created_at__date=d).count())

    # Ishchilar monitoringi
    workers = User.objects.filter(is_staff=True, is_superuser=False)
    for worker in workers:
        worker.active_jobs_count = ServiceRequest.objects.filter(assigned_to=worker, status='ACCEPTED').count()
        worker.completed_jobs_count = ServiceRequest.objects.filter(assigned_to=worker, status='COMPLETED').count()

    context = {
        'total_requests': total_requests,
        'new_requests': new_requests,
        'staff': staff,
        'recent_requests': recent_requests,
        'materials_list': materials,
        'workers': workers,
        'status_counts': status_counts,
        'region_counts': region_counts,
        'activity_labels': activity_labels,
        'activity_data': activity_data,
    }
    return render(request, 'main/dashboard.html', context)

@login_required(login_url='login')
def worker_dashboard(request):
    # Available jobs (NEW)
    available_jobs = ServiceRequest.objects.filter(status='NEW')
    # My jobs (ACCEPTED)
    my_jobs = ServiceRequest.objects.filter(assigned_to=request.user, status='ACCEPTED')
    # Completed jobs
    completed_jobs = ServiceRequest.objects.filter(assigned_to=request.user, status='COMPLETED')
    
    context = {
        'available_jobs': available_jobs,
        'my_jobs': my_jobs,
        'completed_jobs': completed_jobs,
    }
    return render(request, 'main/worker_dashboard.html', context)

@login_required(login_url='login')
def accept_job(request, job_id):
    job = get_object_or_404(ServiceRequest, id=job_id)
    if job.status == 'NEW':
        job.status = 'ACCEPTED'
        job.assigned_to = request.user
        job.save()
        send_client_notification(job.id, 'ACCEPTED')
        messages.success(request, "Ish qabul qilindi!")
    return redirect('worker_dashboard')

@login_required(login_url='login')
def complete_job(request, job_id):
    job = get_object_or_404(ServiceRequest, id=job_id, assigned_to=request.user)
    job.status = 'COMPLETED'
    job.save()
    send_client_notification(job.id, 'COMPLETED')
    messages.success(request, "Ish yakunlandi!")
    return redirect('worker_dashboard')

@login_required(login_url='login')
def reject_job(request, job_id):
    job = get_object_or_404(ServiceRequest, id=job_id, assigned_to=request.user)
    job.status = 'NEW'
    job.assigned_to = None
    job.save()
    send_client_notification(job.id, 'REJECTED')
    messages.warning(request, "Ishdan voz kechildi.")
    return redirect('worker_dashboard')

@login_required(login_url='login')
def mark_processed(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    service_request.status = 'COMPLETED'
    service_request.is_processed = True
    service_request.save()
    messages.success(request, f"Ariza #{request_id} bajarildi deb belgilandi.")
    return redirect('dashboard')

def xizmatlar(request):
    return render(request, 'main/xizmatlar.html')

def haqimizda(request):
    return render(request, 'main/haqimizda.html')

def faq(request):
    return render(request, 'main/faq.html')

def boglanish(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname', '')
        phone = request.POST.get('phone')
        additional_phone = request.POST.get('additional_phone', '')
        region = request.POST.get('region', '')
        district = request.POST.get('district', '')
        mahalla = request.POST.get('mahalla', '')
        street = request.POST.get('street', '')
        house_number = request.POST.get('house_number', '')
        user_identity = request.POST.get('user_identity', 'Jismoniy shaxs')
        service_type = request.POST.get('service_type', 'Boshqa')
        urgency = request.POST.get('urgency', 'LOW')
        message_text = request.POST.get('message', 'Yo\'q')
        preferred_time = request.POST.get('preferred_time', 'Noma\'lum')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')

        if name and phone:
            image = request.FILES.get('image')
            ServiceRequest.objects.create(
                name=name,
                surname=surname,
                phone=phone,
                additional_phone=additional_phone,
                region=region,
                district=district,
                mahalla=mahalla,
                street=street,
                house_number=house_number,
                user_identity=user_identity,
                service_type=service_type,
                urgency=urgency,
                message=message_text,
                preferred_time=preferred_time,
                image=image,
                latitude=lat if lat else None,
                longitude=lon if lon else None
            )
            send_to_admin(
                name=name, surname=surname, phone=phone, region=region,
                user_identity=user_identity, service=service_type, message=message_text,
                preferred_time=preferred_time, additional_phone=additional_phone,
                district=district, mahalla=mahalla, street=street, house_number=house_number,
                urgency=urgency
            )
            messages.success(request, "Murojaatingiz qabul qilindi! Tez orada aloqaga chiqamiz.")
            return redirect('materials_view', service_type=service_type)
            
    return render(request, 'main/boglanish.html')

def vakansiyalar(request):
    return render(request, 'main/vakansiyalar.html')

def yangiliklar(request):
    return render(request, 'main/yangiliklar.html')

def track_order(request):
    orders = None
    phone = None
    if request.method == 'POST':
        phone = request.POST.get('phone')
        if phone:
            orders = ServiceRequest.objects.filter(phone__icontains=phone)
    return render(request, 'main/track_order.html', {'orders': orders, 'phone': phone})

def calculator_view(request):
    prices = ServicePrice.objects.all()
    return render(request, 'main/calculator.html', {'prices': prices})

def submit_review(request, job_id):
    job = get_object_or_404(ServiceRequest, id=job_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if job.assigned_to and job.status == 'COMPLETED':
            Review.objects.create(
                request=job,
                master=Master.objects.filter(name__icontains=job.assigned_to.username).first() or Master.objects.first(),
                rating=rating,
                comment=comment
            )
            messages.success(request, "Sharhingiz uchun rahmat!")
    return redirect('track_order')

def send_client_notification(order_id, status):
    """
    Buyurtma holati o'zgarganda mijozga Telegram orqali xabar yuborish
    """
    try:
        order = ServiceRequest.objects.get(id=order_id)
        phone = order.phone
        if not phone.startswith('+'):
            phone = '+' + phone
        
        tg_user = TelegramUser.objects.filter(phone=phone).first()
        if tg_user:
            send_status_update(tg_user.chat_id, order.id, status)
    except Exception as e:
        print(f"Notification error: {e}")
