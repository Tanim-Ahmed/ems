from django.contrib import admin
from employee_information.models import Department, Position, Employees


# =====================================
# Department Admin
# =====================================
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'status',
        'date_added',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'name',
        'description',
    )


# =====================================
# Position Admin
# =====================================
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'status',
        'date_added',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'name',
        'description',
    )


# =====================================
# Employee Admin
# =====================================
@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):

    list_display = (
        'code',
        'fullname',
        'department_id',
        'position_id',
        'total_hour',
        'total_completion_hour',
        'training_need_to_completed',
        'status',
    )

    search_fields = (
        'code',
        'firstname',
        'middlename',
        'lastname',
        'email',
        'contact',
    )

    list_filter = (
        'department_id',
        'position_id',
        'status',
    )

    readonly_fields = (
        'total_hour',
    )

    fieldsets = (

        ('Personnel Information', {
            'fields': (
                'code',
                'firstname',
                'middlename',
                'lastname',
                'gender',
                'dob',
                'contact',
                'email',
                'address',
                'department_id',
                'position_id',
                'date_hired',
                'salary',
                'status',
            )
        }),

        ('Training Hours', {
            'fields': (
                'safety_training_hours',
                'technical_training_hours',
                'pra_training_hours',
                'ojt_training_hours',
                'total_hour',
            )
        }),

        ('Safety Training', {
            'fields': (
                'safety_training_start_date',
                'safety_training_end_date',
            )
        }),

        ('Technical Training', {
            'fields': (
                'technical_training_start_date',
                'technical_training_end_date',
            )
        }),

        ('PRA Training', {
            'fields': (
                'pra_training_start_date',
                'pra_training_end_date',
            )
        }),

        ('OJT Training', {
            'fields': (
                'ojt_training_start_date',
                'ojt_training_end_date',
            )
        }),

        ('Completion Information', {
            'fields': (
                'total_completion_hour',
                'training_need_to_completed',
            )
        }),

    )

    def fullname(self, obj):
        return f"{obj.firstname} {obj.middlename or ''} {obj.lastname}".strip()

    fullname.short_description = "Personnel Name"