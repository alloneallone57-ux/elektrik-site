from django.urls import path
from . import views

urlpatterns = [
    path('', views.haqimizda, name='index'),
    path('ariza/', views.index, name='ariza'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/worker/', views.worker_dashboard, name='worker_dashboard'),
    path('dashboard/accept/<int:job_id>/', views.accept_job, name='accept_job'),
    path('dashboard/complete/<int:job_id>/', views.complete_job, name='complete_job'),
    path('dashboard/reject/<int:job_id>/', views.reject_job, name='reject_job'),
    path('dashboard/mark/<int:request_id>/', views.mark_processed, name='mark_processed'),
    path('materials/<str:service_type>/', views.materials_view, name='materials_view'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('xizmatlar/', views.xizmatlar, name='xizmatlar'),
    path('haqimizda/', views.haqimizda, name='haqimizda'),
    path('faq/', views.faq, name='faq'),
    path('boglanish/', views.boglanish, name='boglanish'),
    path('vakansiyalar/', views.vakansiyalar, name='vakansiyalar'),
    path('yangiliklar/', views.yangiliklar, name='yangiliklar'),
    path('track-order/', views.track_order, name='track_order'),
    path('submit-review/<int:job_id>/', views.submit_review, name='submit_review'),
    path('calculator/', views.calculator_view, name='calculator'),
]
