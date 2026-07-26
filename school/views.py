from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils import timezone
from .models import Student, Department, Fee
import calendar


@login_required
def dashboard(request):
    today = timezone.now().date()

    # Build last 7 months (year, month) tuples, oldest to newest
    months = []
    for i in range(6, -1, -1):
        month_index = (today.month - i - 1) % 12 + 1
        year_offset = (today.month - i - 1) // 12
        months.append((today.year + year_offset, month_index))

    chart_labels = [calendar.month_abbr[m] for (y, m) in months]

    # Revenue per month — sum of paid fees, grouped by paid_date
    revenue_data = []
    for (y, m) in months:
        total = Fee.objects.filter(
            status='paid', paid_date__year=y, paid_date__month=m
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        revenue_data.append(float(total))

    # Students admitted per month, split by gender
    boys_data = []
    girls_data = []
    for (y, m) in months:
        boys = Student.objects.filter(
            admission_date__year=y, admission_date__month=m, gender='male'
        ).count()
        girls = Student.objects.filter(
            admission_date__year=y, admission_date__month=m, gender='female'
        ).count()
        boys_data.append(boys)
        girls_data.append(girls)

    total_revenue = Fee.objects.filter(status='paid').aggregate(
        total=models.Sum('amount'))['total'] or 0

    context = {
        'total_students': Student.objects.count(),
        'total_awards': 50,
        'total_departments': Department.objects.count(),
        'total_revenue': total_revenue,
        'chart_labels': chart_labels,
        'revenue_data': revenue_data,
        'boys_data': boys_data,
        'girls_data': girls_data,
    }
    return render(request, 'dashboard.html', context)

def home(request):
    return render(request, 'home.html')


@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})


@login_required
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


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    departments = Department.objects.all()

    if request.method == "POST":
        roll_number = request.POST.get("roll_number")

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

        if request.FILES.get("photo"):
            student.photo = request.FILES["photo"]

        student.save()
        messages.success(request, "Student updated successfully.")
        return redirect("student_list")

    return render(request, "edit_student.html", {"student": student, "departments": departments})


@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect("student_list")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def fee_list(request):
    fees = Fee.objects.select_related('student').all().order_by('-due_date')
    total_pending = Fee.objects.filter(status='pending').count()
    total_collected = Fee.objects.filter(status='paid').aggregate(
        total=models.Sum('amount'))['total'] or 0
    return render(request, 'fee_list.html', {
        'fees': fees,
        'total_pending': total_pending,
        'total_collected': total_collected,
    })


@login_required
def add_fee(request):
    students = Student.objects.all()
    if request.method == 'POST':
        Fee.objects.create(
            student_id=request.POST.get('student'),
            fee_type=request.POST.get('fee_type'),
            amount=request.POST.get('amount'),
            due_date=request.POST.get('due_date'),
        )
        messages.success(request, "Fee record added successfully.")
        return redirect('fee_list')
    return render(request, 'add_fee.html', {'students': students})


@login_required
def mark_fee_paid(request, id):
    fee = get_object_or_404(Fee, id=id)
    fee.status = 'paid'
    fee.paid_date = timezone.now().date()
    fee.save()
    messages.success(request, "Fee marked as paid.")
    return redirect('fee_list')