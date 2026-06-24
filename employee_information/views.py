from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from employee_information.models import Department, Position, Employees

import json


# =========================
# LOGIN
# =========================

def login_user(request):
    logout(request)

    resp = {
        "status": "failed",
        "msg": ""
    }

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = 'Incorrect username or password'
        else:
            resp['msg'] = 'Incorrect username or password'

    return HttpResponse(
        json.dumps(resp),
        content_type='application/json'
    )


# =========================
# LOGOUT
# =========================

def logoutuser(request):
    logout(request)
    return redirect('/')


# =========================
# DASHBOARD
# =========================

@login_required
def home(request):

    total_training_hours = (
        Employees.objects.aggregate(
            total=Sum('total_hour')
        )['total'] or 0
    )

    total_completion_hours = (
        Employees.objects.aggregate(
            total=Sum('total_completion_hour')
        )['total'] or 0
    )

    total_pending_training = (
        Employees.objects.aggregate(
            total=Sum('training_need_to_completed')
        )['total'] or 0
    )

    active_employee_count = Employees.objects.filter(
        status=1
    ).count()

    context = {
        'page_title': 'Dashboard',

        'total_department': Department.objects.count(),
        'total_position': Position.objects.count(),
        'total_employee': Employees.objects.count(),

        'active_employee_count': active_employee_count,

        'total_training_hours': total_training_hours,
        'total_completion_hours': total_completion_hours,
        'total_pending_training': total_pending_training,
    }

    return render(
        request,
        'employee_information/home.html',
        context
    )


# =========================
# ABOUT
# =========================

def about(request):
    context = {
        'page_title': 'About',
    }
    return render(
        request,
        'employee_information/about.html',
        context
    )


# =========================
# DEPARTMENTS
# =========================

@login_required
def departments(request):
    context = {
        'page_title': 'Departments',
        'departments': Department.objects.all(),
    }
    return render(
        request,
        'employee_information/departments.html',
        context
    )


@login_required
def manage_departments(request):

    department = {}

    if request.method == "GET":
        id = request.GET.get('id', '')

        if id.isnumeric():
            department = Department.objects.filter(
                id=id
            ).first()

    return render(
        request,
        'employee_information/manage_department.html',
        {'department': department}
    )


@login_required
def save_department(request):

    data = request.POST
    resp = {'status': 'failed'}

    try:

        if data.get('id') and data['id'].isnumeric():

            Department.objects.filter(
                id=data['id']
            ).update(
                name=data['name'],
                description=data['description'],
                status=data['status']
            )

        else:

            Department.objects.create(
                name=data['name'],
                description=data['description'],
                status=data['status']
            )

        resp['status'] = 'success'

    except Exception as e:
        print(e)

    return HttpResponse(
        json.dumps(resp),
        content_type="application/json"
    )


@login_required
def delete_department(request):

    resp = {'status': 'failed'}

    try:
        Department.objects.filter(
            id=request.POST['id']
        ).delete()

        resp['status'] = 'success'

    except Exception as e:
        print(e)

    return HttpResponse(
        json.dumps(resp),
        content_type="application/json"
    )


# =========================
# POSITIONS
# =========================

@login_required
def positions(request):

    context = {
        'page_title': 'Positions',
        'positions': Position.objects.all(),
    }

    return render(
        request,
        'employee_information/positions.html',
        context
    )


@login_required
def manage_positions(request):

    position = {}

    if request.method == "GET":

        id = request.GET.get('id', '')

        if id.isnumeric():
            position = Position.objects.filter(
                id=id
            ).first()

    return render(
        request,
        'employee_information/manage_position.html',
        {'position': position}
    )


@login_required
def save_position(request):

    data = request.POST

    resp = {'status': 'failed'}

    try:

        if data.get('id') and data['id'].isnumeric():

            Position.objects.filter(
                id=data['id']
            ).update(
                name=data['name'],
                description=data['description'],
                status=data['status']
            )

        else:

            Position.objects.create(
                name=data['name'],
                description=data['description'],
                status=data['status']
            )

        resp['status'] = 'success'

    except Exception as e:
        print(e)

    return HttpResponse(
        json.dumps(resp),
        content_type="application/json"
    )


@login_required
def delete_position(request):

    resp = {'status': 'failed'}

    try:
        Position.objects.filter(
            id=request.POST['id']
        ).delete()

        resp['status'] = 'success'

    except Exception as e:
        print(e)

    return HttpResponse(
        json.dumps(resp),
        content_type="application/json"
    )


# =========================
# EMPLOYEES
# =========================

@login_required
def employees(request):

    context = {
        'page_title': 'Employees',
        'employees': Employees.objects.all()
    }

    return render(
        request,
        'employee_information/employees.html',
        context
    )


@login_required
def manage_employees(request):

    employee = {}

    if request.method == "GET":

        id = request.GET.get('id', '')

        if id.isnumeric():
            employee = Employees.objects.filter(
                id=id
            ).first()

    context = {
        'employee': employee,
        'departments': Department.objects.filter(status=1),
        'positions': Position.objects.filter(status=1),
    }

    return render(
        request,
        'employee_information/manage_employee.html',
        context
    )


@login_required
def save_employee(request):

    data = request.POST

    resp = {'status': 'failed'}

    employee_id = data.get('id', '')

    if employee_id and employee_id.isnumeric():
        check = Employees.objects.exclude(
            id=employee_id
        ).filter(code=data['code'])
    else:
        check = Employees.objects.filter(
            code=data['code']
        )

    if check.exists():

        resp['status'] = 'failed'
        resp['msg'] = 'Code Already Exists'

        return HttpResponse(
            json.dumps(resp),
            content_type="application/json"
        )

    try:

        dept = Department.objects.get(
            id=data['department_id']
        )

        pos = Position.objects.get(
            id=data['position_id']
        )

        employee_data = {

            'code': data.get('code'),
            'firstname': data.get('firstname'),
            'middlename': data.get('middlename'),
            'lastname': data.get('lastname'),
            'gender': data.get('gender'),
            'dob': data.get('dob') or None,

            'contact': data.get('contact'),
            'email': data.get('email'),
            'address': data.get('address'),

            'department_id': dept,
            'position_id': pos,

            'date_hired': data.get('date_hired'),
            'salary': float(data.get('salary') or 0),
            'status': int(data.get('status') or 1),

            'safety_training_hours': float(data.get('safety_training_hours') or 0),
            'technical_training_hours': float(data.get('technical_training_hours') or 0),
            'pra_training_hours': float(data.get('pra_training_hours') or 0),
            'ojt_training_hours': float(data.get('ojt_training_hours') or 0),

            'total_hour': float(data.get('total_hour') or 0),

            'safety_training_start_date': data.get('safety_training_start_date') or None,
            'safety_training_end_date': data.get('safety_training_end_date') or None,

            'technical_training_start_date': data.get('technical_training_start_date') or None,
            'technical_training_end_date': data.get('technical_training_end_date') or None,

            'pra_training_start_date': data.get('pra_training_start_date') or None,
            'pra_training_end_date': data.get('pra_training_end_date') or None,

            'ojt_training_start_date': data.get('ojt_training_start_date') or None,
            'ojt_training_end_date': data.get('ojt_training_end_date') or None,

            'total_completion_hour': float(data.get('total_completion_hour') or 0),

            'training_need_to_completed': float(
                data.get('training_need_to_completed') or 0
            ),
        }

        if employee_id and employee_id.isnumeric():

            Employees.objects.filter(
                id=employee_id
            ).update(**employee_data)

        else:

            Employees.objects.create(
                **employee_data
            )

        resp['status'] = 'success'

    except Exception as e:

        resp['status'] = 'failed'
        resp['msg'] = str(e)

        print(e)

    return HttpResponse(
        json.dumps(resp),
        content_type="application/json"
    )


@login_required
def delete_employee(request):

    resp = {'status': 'failed'}

    try:

        Employees.objects.filter(
            id=request.POST['id']
        ).delete()

        resp['status'] = 'success'

    except Exception as e:
        print(e)

    return HttpResponse(
        json.dumps(resp),
        content_type="application/json"
    )


@login_required
def view_employee(request):

    employee = {}

    if request.method == "GET":

        id = request.GET.get('id', '')

        if id.isnumeric():

            employee = Employees.objects.filter(
                id=id
            ).first()

    context = {
        'employee': employee,
        'departments': Department.objects.filter(status=1),
        'positions': Position.objects.filter(status=1),
    }

    return render(
        request,
        'employee_information/view_employee.html',
        context
    )