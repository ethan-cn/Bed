from django.http import JsonResponse
from django.shortcuts import render
import sys, os
from django.utils import timezone
from django.core.paginator import Paginator

work_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, work_dir)
from .models import Patient, Department
from utils.common import my_login

bed_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from bed.models import Bed
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth


@my_login
def redirect_patient(request):
    """
    跳转病人列表信息页
    :param request:
    :return:
    """
    info = get_session_info(request)
    return render(request, 'show_patient.html', {'result': info})


def get_session_info(request):
    result = {}
    username = request.session['username']
    position = request.session['position']
    result['username'] = username
    result['position'] = position
    return result


@my_login
def redirect_new_patient(request):
    """
    跳转入院登记页
    :param request:
    :return:
    """
    result = {}
    username = request.session['username']
    position = request.session['position']
    result['username'] = username
    result['position'] = position
    department_all = []
    departments = Department.objects.all()
    for department in departments:
        department_all.append(department.name)
    beds = Bed.objects.filter(status=0)
    prices = []
    for i in beds:
        prices.append(i.price)
    prices = list(sorted(set(prices)))
    result['prices'] = prices
    result['department'] = department_all
    return render(request, 'new_patient.html', {'result': result})


@my_login
def redirect_department(request):
    """
    跳转入院登记页
    :param request:
    :return:
    """
    info = get_session_info(request)

    return render(request, 'show_department.html', {'result': info})


@my_login
def redirect_new_department(request):
    """
    跳转入院登记页
    :param request:
    :return:
    """
    info = get_session_info(request)

    return render(request, 'new_department.html', {'result': info})


def query_department(req):
    """
    查询入院信息详情页
    :param req:
    :return:
    """
    response_data = {}
    page = req.GET.get('page')
    dict_values = {}
    results = Paginator(Department.objects.all(), per_page=4).page(page)
    total = Paginator(Department.objects.all(), per_page=4).num_pages
    if results:
        for result in results:
            dict_values[result.department_id] = {
                'id': result.department_id,
                'name': result.name,
                'addr': result.addr,
                'doctor_name': result.doctor_name,
            }
    else:
        response_data = {'error': '获取科室信息失败！', 'message': '找不到科室信息'}
        return JsonResponse(response_data, status=403)
    response_data['department'] = list(sorted(dict_values.values(), key=lambda item: item['id']))
    response_data["total"] = total
    return JsonResponse(response_data)


def query_patient(req):
    """
    查询入院信息详情页
    :param req:
    :return:
    """
    response_data = {}
    page = req.GET.get('page')
    dict_values = {}
    results = Paginator(Patient.objects.all(), per_page=4).page(page)
    total = Paginator(Patient.objects.all(), per_page=4).num_pages
    if results:
        for result in results:
            if result.gender == 0:
                sex = '男'
            else:
                sex = '女'
            if not result.patient_bed_id_id:
                bed_name = '已出院'
            else:
                bed_info = Bed.objects.filter(bed_id=result.patient_bed_id_id).first()
                bed_name = bed_info.bed_name
            dict_values[result.patient_id] = {
                'id': result.patient_id,
                'name': result.name,
                'age': result.age,
                'gender': sex,
                'department': result.department,
                'description': result.description,
                'bedroom': bed_name,
                'created': result.created.strftime('%Y-%m-%d %H:%M'),
                'modified': result.modified.strftime('%Y-%m-%d %H:%M')
            }
    else:
        response_data = {'error': '获取入住病人信息失败！', 'message': '找不到病人信息'}
        return JsonResponse(response_data, status=403)
    response_data['patient'] = list(sorted(dict_values.values(), key=lambda item: item['id']))
    response_data["total"] = total
    return JsonResponse(response_data)


def get_department_by_name(request):
    """
    通过用户名模糊查询用户信息
    :return:
    """
    response_data = {}
    response_data['user'] = []
    dict_values = {}
    page = request.GET.get('page')
    name = request.GET.get('name')
    results = Paginator(Department.objects.filter(name__contains=name), per_page=4).page(page)
    total = Paginator(Department.objects.filter(name__contains=name), per_page=4).num_pages
    if results:
        for result in results:
            dict_values[result.department_id] = {
                'id': result.department_id,
                'name': result.name,
                'doctor_name': result.doctor_name,
                'addr': result.addr,

            }
    else:
        response_data = {'error': '获取用户信息失败！', 'message': '找不到用户信息.'}
        return JsonResponse(response_data, status=403)
    response_data['department'] = list(dict_values.values())
    response_data["total"] = total
    return JsonResponse(response_data)


@csrf_exempt
def add_patient(request):
    """
    新增入院管理
    :param request:
    :return:
    """
    name = request.POST.get('name')
    gender = request.POST.get('gender')
    if gender == '男':
        gender = 0
    else:
        gender = 1
    age = request.POST.get('age')
    price = request.POST.get('price')[:-1]
    department = request.POST.get('department')
    description = request.POST.get('description')
    create_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    modify_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    beds = Bed.objects.filter(price=price)
    bed_ids = []
    for bed in beds:
        if bed.status != 1:
            bed_id = bed.bed_id
            bed_ids.append(bed_id)
    if len(bed_ids) <= 0:
        return JsonResponse({'message': '当前价格的床位空缺，请重新选择其他价格的床位'}, status=401)
    bed_id = bed_ids[0]
    Bed.objects.filter(bed_id=bed_id).update(status=1)
    Patient.objects.create(
        name=name,
        gender=gender,
        age=age,
        patient_bed_id_id=bed_id,
        department=department,
        description=description,
        created=create_time,
        modified=modify_time
    )
    info = get_session_info(request)

    return render(request, "show_patient.html", {'result': info})


@csrf_exempt
def add_department(request):
    name = request.POST.get('name')
    doctor_name = request.POST.get('doctor_name')
    addr = request.POST.get('addr')

    Department.objects.create(
        name=name,
        doctor_name=doctor_name,
        addr=addr,
    )
    info = get_session_info(request)

    return render(request, "show_department.html", {'result': info})

import traceback

@csrf_exempt
def modify_patient(request):
    """
    修改用户信息
    :return:
    """
    response_data = {}
    try:
        patient_id = request.POST.get('id')
        bed_name = request.POST.get('bed_name')
        print("=========="+bed_name)
        price = request.POST.get('price')[:-1]
        # price = request.POST.get('price')
        # print(price)
        # price = 100
        beds = Bed.objects.filter(price=price)
        bed_ids = []
        for bed in beds:
            if bed.status != 1:
                bed_id = bed.bed_id
                bed_ids.append(bed_id)
        if len(bed_ids) <= 0:
            response_data['message'] = '当前价位床位已无空余，请选择其他价位的床位！'
            return JsonResponse(response_data, status=401)
        bed_id = bed_ids[0]
        Bed.objects.filter(bed_id=bed_id).update(status=1)
        Bed.objects.filter(bed_name=bed_name).update(status=0)
        Patient.objects.filter(patient_id=patient_id).update(
            patient_bed_id_id=bed_id)
        response_data['message'] = '修改成功'
        return JsonResponse(response_data, status=201)
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        response_data['message'] = '修改失败'
        return JsonResponse(response_data, status=401)


@csrf_exempt
def modify_department(request):
    """
    修改用户信息
    :return:
    """
    response_data = {}
    try:
        department_id = request.POST.get('userId')
        name = request.POST.get('name')
        doctor_name = request.POST.get('doctor_name')
        addr = request.POST.get('addr')
        Department.objects.filter(department_id=department_id).update(
            doctor_name=doctor_name,
            name=name,
            addr=addr)
        response_data['message'] = '修改成功'
        return JsonResponse(response_data, status=201)
    except Exception as e:
        print(e)
        response_data['message'] = '修改失败'
        return JsonResponse(response_data, status=401)


@csrf_exempt
def get_patient_by_id(request):
    """
    通过id模糊查询用户信息
    :return:
    """
    response_data = {}
    response_data['patient'] = []
    patient_id = request.GET.get('id')
    results = Patient.objects.filter(patient_id=patient_id)
    dict_value = {}
    if results:
        for result in results:
            bed = Bed.objects.filter(bed_id=result.patient_bed_id_id)
            for i in bed:
                bed_name = i.bed_name
            dict_value['id'] = result.patient_id
            dict_value['bed_name'] = bed_name
            dict_value['name'] = result.name
    else:
        response_data = {'error': '获取用户信息失败！', 'message': '找不到用户信息.'}
        return JsonResponse(response_data, status=403)
    response_data['patient'] = dict_value
    return JsonResponse(response_data)


@csrf_exempt
def get_department_by_id(request):
    response_data = {}
    response_data['department'] = []
    department_id = request.GET.get('department_id')
    results = Department.objects.filter(department_id=department_id)
    dict_value = {}
    if results:
        for result in results:
            dict_value['id'] = result.department_id
            dict_value['name'] = result.name
            dict_value['doctor_name'] = result.doctor_name
            dict_value['addr'] = result.addr
    else:
        response_data = {'error': '获取科室信息失败！', 'message': '找不到科室信息.'}
        return JsonResponse(response_data, status=403)
    response_data['department'] = dict_value
    return JsonResponse(response_data)


@csrf_exempt
def delete_patient(request):
    """
    停床
    :return:
    """
    response_data = {}
    try:
        patient_id = request.POST.get('patient_id')
        patients = Patient.objects.filter(patient_id=patient_id)
        for i in patients:
            bed_id = i.patient_bed_id_id
        Bed.objects.filter(bed_id=bed_id).update(status=0)
        modify_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        patients.update(
            patient_bed_id_id='',
            modified=modify_time)
        response_data['message'] = '修改成功'
        return JsonResponse(response_data, status=201)
    except Exception as e:
        print(e)
        response_data['message'] = '修改失败'
        return JsonResponse(response_data, status=401)


@csrf_exempt
def delete_department(request):
    """
    停床
    :return:
    """
    response_data = {}
    department_id = request.POST.get('department_id')
    result = Department.objects.filter(department_id=department_id).first()
    try:
        if not result:
            response_data = {'error': '删除科室失败！', 'message': '找不到id为%s的科室' % department_id}
            return JsonResponse(response_data, status=403)
        result.delete()
        response_data = {'message': '删除成功！'}
        return JsonResponse(response_data, status=201)
    except Exception as e:
        response_data = {'message': '删除失败！'}
        return JsonResponse(response_data, status=403)


def get_patient_by_name(request):
    """
    通过名称模糊查询患者信息
    :return:
    """
    response_data = {}
    response_data['user'] = []
    dict_values = {}
    page = request.GET.get('page')
    name = request.GET.get('name')
    results = Paginator(Patient.objects.filter(name__contains=name), per_page=4).page(page)
    total = Paginator(Patient.objects.filter(name__contains=name), per_page=4).num_pages
    if results:
        for result in results:
            if result.gender == 0:
                sex = '男'
            else:
                sex = '女'
            if not result.patient_bed_id_id:
                bed_name = '已出院'
            else:
                bed_info = Bed.objects.filter(bed_id=result.patient_bed_id_id).first()
                bed_name = bed_info.bed_name
            dict_values[result.patient_id] = {
                'id': result.patient_id,
                'name': result.name,
                'age': result.age,
                'gender': sex,
                'department': result.department,
                'description': result.description,
                'bedroom': bed_name,
                'created': result.created.strftime('%Y-%m-%d %H:%M'),
                'modified': result.modified.strftime('%Y-%m-%d %H:%M')
            }
    else:
        response_data = {'error': '获取用户信息失败！', 'message': '找不到用户信息.'}
        return JsonResponse(response_data, status=403)
    response_data['patient'] = list(dict_values.values())
    response_data["total"] = total
    return JsonResponse(response_data)
