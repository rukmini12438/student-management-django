from django.shortcuts import render, redirect
from .models import Student, Department

def dashboard(request):
    context = {
        'total_students': Student.objects.count(),
        'total_awards': 50,
        'total_departments': Department.objects.count(),
        'total_revenue': 505,
    }
    return render(request, 'dashboard.html', context)

def home(request):
    return render(request, 'home.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def add_student(request):
    departments = Department.objects.all()

    if request.method == 'POST':
        Student.objects.create(
            # Basic Info
            name=request.POST['name'],
            roll_number=request.POST['roll_number'],
            date_of_birth=request.POST.get('date_of_birth') or None,
            gender=request.POST.get('gender', ''),
            blood_group=request.POST.get('blood_group', ''),
            photo=request.FILES.get('photo'),

            # Academic Info
            course=request.POST['course'],
            department_id=request.POST.get('department') or None,
            admission_date=request.POST.get('admission_date') or None,
            age=request.POST['age'],

            # Contact Info
            email=request.POST['email'],
            phone_number=request.POST.get('phone_number', ''),
            address=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
            state=request.POST.get('state', ''),
            pincode=request.POST.get('pincode', ''),

            # Father's Details
            father_name=request.POST.get('father_name', ''),
            father_occupation=request.POST.get('father_occupation', ''),
            father_phone=request.POST.get('father_phone', ''),

            # Mother's Details
            mother_name=request.POST.get('mother_name', ''),
            mother_occupation=request.POST.get('mother_occupation', ''),
            mother_phone=request.POST.get('mother_phone', ''),

            # Guardian Details
            guardian_name=request.POST.get('guardian_name', ''),
            guardian_relation=request.POST.get('guardian_relation', ''),
            guardian_phone=request.POST.get('guardian_phone', ''),
        )
        return redirect('student_list')

    return render(request, 'add_student.html', {'departments': departments})