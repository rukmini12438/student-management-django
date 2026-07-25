from django.contrib import admin
from .models import Student, Department, Fee

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'course', 'department', 'gender', 'is_active')
    list_filter = ('course', 'department', 'gender', 'is_active')
    search_fields = ('name', 'roll_number', 'father_name', 'mother_name')

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'roll_number', 'date_of_birth', 'gender', 'blood_group', 'photo')
        }),
        ('Academic Info', {
            'fields': ('course', 'department', 'admission_date', 'age')
        }),
        ('Contact Info', {
            'fields': ('email', 'phone_number', 'address', 'city', 'state', 'pincode')
        }),
        ("Father's Details", {
            'fields': ('father_name', 'father_occupation', 'father_phone')
        }),
        ("Mother's Details", {
            'fields': ('mother_name', 'mother_occupation', 'mother_phone')
        }),
        ('Guardian Details', {
            'fields': ('guardian_name', 'guardian_relation', 'guardian_phone'),
            'classes': ('collapse',),
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_of_department', 'created_at')
    search_fields = ('name',)


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'status', 'due_date', 'paid_date')
    list_filter = ('status',)
    search_fields = ('student__name',)