"""ProjektBase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ProjektApp import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home_view, name='home_view'),
    path('zad1/', views.zad1_view, name='zad1'),
    path('zad2/', views.zad2, name='zad2'),
    path('add_user/', views.add_user, name='add_user'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('subject/edit_status/<int:subject_id>/<int:student_id>/', views.edit_status, name='edit_status'),
    path('subjects/', views.lista_predmeta, name='lista_predmeta'),
    path('admin/', admin.site.urls),
    path('subjects/<int:predmet_id>/promjena/', views.promjena_predmeta, name='promjena_predmeta'),
    path('subjects/<int:predmet_id>/popis_studenata/', views.popis_studenata, name='popis_studenata'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('subject/remove_subject_students/<int:subject_id>/', views.remove_subject_students, name='remove_subject_student'),
    path('enrollments/create/', views.create_enrollment, name='create_enrollment'),
    path('professor_list/', views.professor_list, name='professor_list'),
    path('student_list/', views.student_list, name='student_list'),
    path('enrollment_list/<int:student_id>/', views.enrollment_list, name='enrollment_list'),
    path('edit_professor/<int:professor_id>/', views.edit_professor, name='edit_professor'),
    path('enrolled_student/', views.enrolled_student, name='enrolled_student'),
    path('professor/subjects/', views.professor_subjects, name='professor_subjects'),
    path('subject/student_list/<int:subject_id>/', views.subject_student_list, name='subject_student_list'),
    path('subject_list/<int:subject_id>/', views.passed_subject_details, name='passed_subject_details'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('subject/enrolled_students/<int:subject_id>/', views.subject_enrolled_students, name='subject_enrolled_students'),
    path('subject/remove_subject_student/<int:subject_id>/<int:student_id>/', views.remove_subject_student, name='remove_subject_student'),
    path('remove_user/', views.remove_user, name='remove_user'),
    path('edit_status_fail/<str:status>/', views.edit_status_fail, name='edit_status_fail'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('success/', views.success_login, name='success'),
    path('forbidden/', views.forbidden, name='forbidden'),
    path('enroll_subject/<int:subject_id>/', views.enroll_subject, name='enroll_subject'),
    path('subject/details/<int:subject_id>/', views.subject_details, name='subject_details'),
    path('unenrolled_subjects/', views.unenrolled_subjects, name='unenrolled_subjects'),
    path('remove_subjects_students/<int:subject_id>/', views.remove_subjects_students, name='remove_subjects_students'),
    path('users/', views.user_list, name='user_list'),
    path('subject_list/', views.subject_list, name='subject_list'),
    path('upisni_list/', views.upisni_list, name='upisni_list'),
    path('subject/passed_students/<int:subject_id>/', views.subject_passed_students, name='subject_passed_students'),
    path('enrollment_success/', views.enrollment_success, name='enrollment_success'),
    path('logout/', views.logout_view, name='logout'),
    path('subject/failed_students/<int:subject_id>/', views.subject_failed_students, name='subject_failed_students'),
]