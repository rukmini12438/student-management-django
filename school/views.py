from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
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


def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    departments = Department.objects.all()

    if request.method == "POST":
        roll_number = request.POST.get("roll_number")

        # Check uniqueness, but allow keeping the same roll number
        if Student.objects.filter(roll_number=roll_number).exclude(id=id).exists():
            messages.error(request, "That roll number is already taken by another student.")
            return render(request, "edit_student.html", {"student": student, "departments": departments})

        student.name = request.POST.get("name")
        student.roll_number = roll_number
        student.date_of_birth = request.POST.get("date_of_birth")
        student.gender = request.POST.get("gender")
        student.blood_group = request.POST.get("blood_group")
        student.course = request.POST.get("course")
        student.department_id = request.POST.get("department")
        student.admission_date = request.POST.get("admission_date")
        student.age = request.POST.get("age")
        student.email = request.POST.get("email")
        student.phone_number = request.POST.get("phone_number")
        student.address = request.POST.get("address")
        student.city = request.POST.get("city")
        student.state = request.POST.get("state")
        student.pincode = request.POST.get("pincode")
        student.father_name = request.POST.get("father_name")
        student.father_occupation = request.POST.get("father_occupation")
        student.father_phone = request.POST.get("father_phone")
        student.mother_name = request.POST.get("mother_name")
        student.mother_occupation = request.POST.get("mother_occupation")
        student.mother_phone = request.POST.get("mother_phone")
        student.guardian_name = request.POST.get("guardian_name")
        student.guardian_relation = request.POST.get("guardian_relation")
        student.guardian_phone = request.POST.get("guardian_phone")

        # Only update photo if a new one was uploaded
        if request.FILES.get("photo"):
            student.photo = request.FILES["photo"]

        student.save()
        messages.success(request, "Student updated successfully.")
        return redirect("student_list")

    return render(request, "edit_student.html", {"student": student, "departments": departments})


def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect("student_list")