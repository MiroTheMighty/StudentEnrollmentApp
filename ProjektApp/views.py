from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.forms import formset_factory
from django.urls import reverse
from .models import Korisnici, Predmeti, StudentEnrollment
from .forms import PredmetForm, KorisniciForm, StudentEnrollmentForm, StudentEnrollmentForm1, StudentEnrollmentForm2
from django.db.models import Sum
from django.http import HttpResponse
from django.db.models import Q, Count
# Create your views here.

def is_admin(user):
    return user.role == 'administrator'

def is_profesor(user):
     return user.role == 'profesor'

def is_student(user):
     return user.role == 'student'

def home_view(request):
    return render(request, 'index.html')

@login_required
def success_login(request):
    user = request.user
    if user.role == 'administrator':
        return render(request, 'success.html', {'user': user})
    elif user.role == 'student':
        return render(request, 'success_student.html', {'user': user})
    elif user.role == 'profesor':
        return render(request, 'success_professor.html', {'user': user})   
    else:
        return redirect('/accounts/login/')

@login_required
def logout_view(request):
        logout(request)
        return redirect('/accounts/login/')

@login_required
@user_passes_test(is_admin)
def student_list(request):
    students = Korisnici.get_students()
    return render(request, 'student_list.html', {'students': students})

@login_required
@user_passes_test(is_admin)
def lista_predmeta(request):
    predmeti = Predmeti.objects.all()
    return render(request, 'lista_predmeta.html', {'predmeti': predmeti})

@login_required
@user_passes_test(is_admin)
def professor_list(request):
    professors = Korisnici.get_professors()
    return render(request, 'professor_list.html', {'professors': professors})

@login_required
@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        role = request.POST['role']
        status = request.POST['status']

        if password != repeat_password:
            error_message = "Passwords do not match."
            return render(request, 'add_user.html', {'error_message': error_message})

        user = Korisnici.objects.create_user(username=username, password=password,
                                             first_name=first_name, last_name=last_name,
                                             email=email, role=role, status=status)
        return redirect('/success/')

    return render(request, 'add_user.html')
    
@login_required
@user_passes_test(is_admin)
def add_subject(request):
    if request.method == 'POST':
        form = PredmetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/success/') 
    else:
        form = PredmetForm()
    
    context = {
        'form': form,
        'professors': Korisnici.objects.filter(role='profesor')
    }
    return render(request, 'add_subject.html', context)

@login_required
@user_passes_test(is_admin)
def promjena_predmeta(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    form = PredmetForm(request.POST or None, instance=predmet)
    if form.is_valid():
        form.save()
        return redirect('lista_predmeta')
    return render(request, 'promjena_predmeta.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_student(request, student_id):
    student = get_object_or_404(Korisnici, id=student_id)
    form = KorisniciForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'edit_student.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def enrollment_list(request, student_id):
    student = get_object_or_404(Korisnici, id=student_id)
    EnrollmentFormSet = formset_factory(StudentEnrollmentForm, extra=0)
    
    if request.method == 'POST':
        formset = EnrollmentFormSet(request.POST)
        
        if formset.is_valid():
            StudentEnrollment.objects.filter(student=student).delete()
            
            for form in formset:
                enrollment = form.save(commit=False)
                enrollment.student = student
                enrollment.save()
            
            return redirect('success')
    else:
        enrollments = StudentEnrollment.objects.filter(student=student)
        initial_data = [{'subject': enrollment.subject, 'status': enrollment.status} for enrollment in enrollments]
        formset = EnrollmentFormSet(initial=initial_data)
    
    context = {
        'student': student,
        'formset': formset
    }
    return render(request, 'enrollment_list.html', context)

@login_required
@user_passes_test(is_admin)
def create_enrollment(request):
    if request.method == 'POST':
        form = StudentEnrollmentForm1(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = StudentEnrollmentForm1()

    students = Korisnici.objects.filter(role='student')
    context = {
        'form': form,
        'students': students
    }
    return render(request, 'create_enrollment.html', context)

@login_required
@user_passes_test(is_admin)
def edit_professor(request, professor_id):
    professor = get_object_or_404(Korisnici, id=professor_id)
    form = KorisniciForm(request.POST or None, instance=professor)
    if form.is_valid():
        form.save()
        return redirect('profesor_list')
    return render(request, 'edit_professor.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def popis_studenata(request, predmet_id):
    predmet = get_object_or_404(Predmeti, id=predmet_id)
    enrollments = StudentEnrollment.objects.filter(subject=predmet)
    return render(request, 'popis_studenata.html', {'predmet': predmet, 'enrollments': enrollments})

@login_required
@user_passes_test(is_admin)
def remove_subjects_students(request, subject_id):
    subject = get_object_or_404(Predmeti, id=subject_id)
    enrollments = StudentEnrollment.objects.filter(subject=subject)

    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        enrollment = get_object_or_404(StudentEnrollment, id=enrollment_id)
        enrollment.delete()
        return redirect('popis_studenata', predmet_id=subject_id)

    context = {'predmet': subject, 'enrollments': enrollments}
    return render(request, 'popis_studenata_admin.html', context)

@login_required
@user_passes_test(is_admin)
def user_list(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = Korisnici.objects.get(id=user_id)
        user.delete()
        return redirect('user_list')

    users = Korisnici.objects.exclude(role="administrator").order_by('status')
    return render(request, 'user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def remove_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = Korisnici.objects.get(id=user_id)
        user.delete()
    return redirect('user_list')

@login_required
@user_passes_test(is_profesor)
def professor_subjects(request):
    list = Predmeti.objects.filter(nositelj=request.user)
    context = {
        'list': list
    }
    return render(request, 'professor_subject.html', context)

@login_required
@user_passes_test(is_profesor)
def subject_student_list(request, subject_id):
    subject = get_object_or_404(Predmeti, id=subject_id)
    enrollments = StudentEnrollment.objects.filter(subject=subject)
    students = [enrollment.student for enrollment in enrollments]
    context = {
        'subject': subject,
        'students': students
    }
    return render(request, 'subject_student_list.html', context)

@login_required
@user_passes_test(is_profesor)
def edit_status(request, subject_id, student_id):
    student = get_object_or_404(Korisnici, id=student_id, role="student")
    subject = get_object_or_404(Predmeti, id=subject_id)
    enrollment = get_object_or_404(StudentEnrollment, student=student, subject=subject)

    if enrollment.status == 'Failed' or enrollment.status == 'Passed':
        return redirect(reverse('edit_status_fail', args=[enrollment.status]))

    if request.method == 'POST':
        form = StudentEnrollmentForm2(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('subject_student_list', subject_id=subject_id)
    else:
        form = StudentEnrollmentForm2(instance=enrollment)

    context = {
        'form': form,
        'subject': subject,
        'student': student,
    }

    return render(request, 'edit_status.html', context)

@login_required
@user_passes_test(is_profesor)
def remove_subject_student(request, subject_id, student_id):
    student = get_object_or_404(Korisnici, id=student_id, role="student")
    subject = get_object_or_404(Predmeti, id=subject_id)
    enrollment = get_object_or_404(StudentEnrollment, student=student, subject=subject)

    if enrollment.status == "Enrolled":
        if request.method == 'POST':
            enrollment.delete()
            return redirect('professor_subjects')

        return render(request, 'remove_subject_student.html', {'subject': subject, 'student': student})

    
    return redirect('forbidden')

@login_required
@user_passes_test(is_profesor)
def forbidden(request):
    return render(request, 'forbidden.html')

def edit_status_fail(request, status):
    context = {'status': status}
    return render(request, 'edit_status_fail.html', context)

@login_required
@user_passes_test(is_profesor)
def subject_passed_students(request, subject_id):
    subject = get_object_or_404(Predmeti, id=subject_id)
    passed_students = Korisnici.objects.filter(studentenrollment__subject=subject, studentenrollment__status='Passed')

    context = {
        'subject': subject,
        'passed_students': passed_students,
    }

    return render(request, 'subject_passed_students.html', context)

@login_required
@user_passes_test(is_profesor)
def subject_enrolled_students(request, subject_id):
    subject = get_object_or_404(Predmeti, id=subject_id)
    enrolled_students = Korisnici.objects.filter(studentenrollment__subject=subject, studentenrollment__status='Enrolled')

    context = {
        'subject': subject,
        'enrolled_students': enrolled_students,
    }

    return render(request, 'subject_enrolled_students.html', context)

@login_required
@user_passes_test(is_profesor)
def subject_failed_students(request, subject_id):
    subject = get_object_or_404(Predmeti, id=subject_id)
    failed_students = Korisnici.objects.filter(studentenrollment__subject=subject, studentenrollment__status='Failed')

    context = {
        'subject': subject,
        'failed_students': failed_students,
    }

    return render(request, 'subject_failed_students.html', context)

@login_required
@user_passes_test(is_profesor)
def subject_details(request, subject_id):
    subject = get_object_or_404(Predmeti, id=subject_id)

    context = {
        'subject': subject,
    }

    return render(request, 'subject_details.html', context)

@login_required
@user_passes_test(is_student)
def upisni_list(request):
    student = request.user
    enrolled_subjects = Predmeti.objects.filter(studentenrollment__student=student, studentenrollment__status="Enrolled")
    passed_subjects = Predmeti.objects.filter(studentenrollment__student=student, studentenrollment__status="Passed")
    failed_subjects = Predmeti.objects.filter(studentenrollment__student=student, studentenrollment__status="Failed")

    passed_ects_total = passed_subjects.aggregate(total_ects=Sum('ects')).get('total_ects') or 0

    context = {
        'enrolled_subjects': enrolled_subjects,
        'passed_subjects': passed_subjects,
        'failed_subjects': failed_subjects,
        'passed_ects_total': passed_ects_total
    }

    return render(request, 'upisni_list.html', context)

@login_required
@user_passes_test(is_student)
def enrolled_student(request):
    student = request.user
    enrolled_subjects = Predmeti.objects.filter(studentenrollment__student=student, studentenrollment__status="Enrolled")

    context = {
        'enrolled_subjects': enrolled_subjects
    }
    return render(request, 'enrolled_student.html', context)

@login_required
@user_passes_test(is_student)
def remove_subject_students(request, subject_id):
    student = request.user
    subject = get_object_or_404(Predmeti, id=subject_id)
    enrollment = get_object_or_404(StudentEnrollment, student=student, subject=subject)

    if enrollment.status == "Enrolled":
        if request.method == 'POST':
            enrollment.delete()
            return redirect('enrolled_student')

        context = {'subject': subject}
        return render(request, 'remove_subject_student.html', context)

    return redirect('forbidden')

@login_required
@user_passes_test(is_student)
def unenrolled_subjects(request):
    student = request.user
    all_subjects = Predmeti.objects.exclude(studentenrollment__student=student).order_by('semester')

    context = {
        'all_subjects': all_subjects
    }
    return render(request, 'unenrolled_subjects.html', context)

@login_required
@user_passes_test(is_student)
def unenrolled_subjects(request):
    student = request.user
    student_status = student.status

    if student_status == 'redovan':
        context = {
            'student': student,
            'student_status': student_status,
            'all_subjects': Predmeti.objects.exclude(studentenrollment__student=student).order_by('sem_red')
        }
    else:
        context = {
            'student': student,
            'student_status': student_status,
            'all_subjects': Predmeti.objects.exclude(studentenrollment__student=student).order_by('sem_izv')
        }

    return render(request, 'unenrolled_subjects.html', context)

@login_required
@user_passes_test(is_student)
def enroll_subject(request, subject_id):
    student = request.user
    subject = get_object_or_404(Predmeti, id=subject_id)
    
    if request.method == 'POST':
        enrollment = StudentEnrollment.objects.create(student=student, subject=subject, status="Enrolled")
        enrollment.save()
        return redirect('unenrolled_subjects')

    return render(request, 'enroll_subject.html', {'subject': subject})

@login_required
@user_passes_test(is_admin)
def subject_list(request):
    subjects = Predmeti.objects.all()
    subject_data = []

    for subject in subjects:
        subject_id = subject.id
        passed_students = StudentEnrollment.objects.filter(subject=subject, status="Passed")
        regular_students = passed_students.filter(student__status="redovan")
        non_regular_students = passed_students.filter(student__status="izvanredan")

        subject_info = {
            'subject_id': subject_id,
            'subject': subject,
            'total_passed': passed_students.count(),
            'regular_passed': regular_students.count(),
            'non_regular_passed': non_regular_students.count()
        }

        subject_data.append(subject_info)

    return render(request, 'subject_list.html', {'subject_data': subject_data})

@login_required
@user_passes_test(is_admin)
def passed_subject_details(request, subject_id):
    subject = Predmeti.objects.get(id=subject_id)
    passed_students = StudentEnrollment.objects.filter(subject=subject, status="Passed")
    regular_students = passed_students.filter(student__status="redovan")
    non_regular_students = passed_students.filter(student__status="izvanredan")
    
    return render(request, 'passed_subject_details.html', {'subject': subject, 'regular_students': regular_students, 'non_regular_students': non_regular_students})

@login_required
@user_passes_test(is_student)
def enrollment_success(request):
    return render(request, 'enrollment_success.html')

@login_required
@user_passes_test(is_student)
def zad2(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        subject_id = request.POST.get('subject_id')

        student = Korisnici.objects.get(id=student_id)
        subject = Predmeti.objects.get(id=subject_id)

        first_year_subjects_regular = Predmeti.objects.filter(sem_red__in=[1, 2])
        first_year_subjects_irregular = Predmeti.objects.filter(sem_izv__in=[1, 2])

        if student.status == "redovan":
            if subject.sem_red in [5, 6]:
                passed_first_year_subjects = StudentEnrollment.objects.filter(
                    student=student,
                    subject__in=first_year_subjects_regular,
                    status="Passed"
                )
                if passed_first_year_subjects.count() != first_year_subjects_regular.count():
                    return HttpResponse("Ne možete upisati treću godinu")
        else:
            if subject.sem_izv in [5, 6]:
                passed_first_year_subjects = StudentEnrollment.objects.filter(
                    student=student,
                    subject__in=first_year_subjects_irregular,
                    status="Passed"
                )
                if passed_first_year_subjects.count() != first_year_subjects_irregular.count():
                    return HttpResponse("Ne možete upisati treću godinu")
                
        if StudentEnrollment.objects.filter(student=student, subject=subject).exists():
            return HttpResponse("Već ste upisani u ovaj predmet.")

        enrollment = StudentEnrollment(student=student, subject=subject, status="Enrolled")
        enrollment.save()

        return redirect('enrollment_success')
    else:
        student = request.user

        if student.status == "redovan":
            subjects = Predmeti.objects.filter(sem_red__in=[5, 6])
        else:
            subjects = Predmeti.objects.filter(sem_izv__in=[5, 6])

        return render(request, 'enable_enrollment.html', {'subjects': subjects})


def zad1():
    students_with_ects = Korisnici.objects.filter(
        role="student",
        studentenrollment__status='Enrolled'
    ).annotate(
        total_ects=Sum('studentenrollment__subject__ects')
    ).filter(
        total_ects__gt=30
    )

    return students_with_ects

def zad1_view(request):
    students_over_30_ects = zad1()
    return render(request, 'students_over_30_ects.html', {'students': students_over_30_ects})

