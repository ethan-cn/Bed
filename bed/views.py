from django.http import JsonResponse
from django.shortcuts import render
import sys, os
from django.utils import timezone
from django.core.paginator import Paginator
from utils.common import my_login

work_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, work_dir)
from .models import Bed
from patient.models import Patient, Department
from django.views.decorators.csrf import csrf_exempt


@my_login
def redirect_bed(request):
    info = get_session_info(request)
    return render(request, 'show_bed.html', {'result': info})


@my_login
def redirect_new_bed(request):
    result = {}
    username = request.session['username']
    position = request.session['position']
    result['username'] = username
    result['position'] = position
    department_all = []
    departments = Department.objects.all()
    for department in departments:
        department_all.append(department.name)
    result['department'] = department_all
    return render(request, 'new_bed.html', {'result': result})


def query_bed(request):
    """
        查询入院信息详情页
        :param req:
        :return:
        """
    response_data = {}
    page = request.GET.get('page')
    dict_values = {}
    results = Paginator(Bed.objects.all(), per_page=4).page(page)
    total = Paginator(Bed.objects.all(), per_page=4).num_pages
    if results:
        for result in results:
            patient_info = Patient.objects.filter(patient_bed_id_id=result.bed_id).first()
            if patient_info:
                patient_name = patient_info.name
            else:
                patient_name = '无'
            if result.status == 0:
                status = '空床'
            else:
                status = '已入住'
            dict_values[result.bed_id] = {
                'id': result.bed_id,
                'name': result.bed_name,
                'price': result.price,
                'status': status,
                'patient_name': patient_name,
            }
    else:
        response_data = {'error': '获取床位信息失败！', 'message': '找不到床位信息'}
        return JsonResponse(response_data, status=403)
    response_data['bed'] = list(sorted(dict_values.values(), key=lambda item: item['id']))
    response_data["total"] = total
    return JsonResponse(response_data)


@csrf_exempt
def add_bed(request):
    """
    新增床位
    :param request:
    :return:
    """
    name = request.POST.get('name')
    price = request.POST.get('price')
    price = price[:-1]
    status = 0
    Bed.objects.create(
        bed_name=name,
        price=price,
        status=status,

    )
    info = get_session_info(request)

    return render(request, "show_bed.html", {'result': info})


def get_session_info(request):
    result = {}
    username = request.session['username']
    position = request.session['position']
    result['username'] = username
    result['position'] = position
    return result


@csrf_exempt
def delete_bed(request):
    """
    删除用户信息
    :param user_id: 用户id
    :return:
    """
    bed_id = request.POST.get('bed_id')
    result = Bed.objects.filter(bed_id=bed_id).first()
    try:
        if not result:
            response_data = {'error': '删除床位失败！', 'message': '找不到id为%s的床位' % bed_id}
            return JsonResponse(response_data, status=403)
        result.delete()
        response_data = {'message': '删除成功！'}
        return JsonResponse(response_data, status=201)
    except Exception as e:
        response_data = {'message': '删除失败！'}
        return JsonResponse(response_data, status=403)


@csrf_exempt
def modify_bed(request):
    """
    修改用户信息
    :return:
    """
    response_data = {}
    try:
        bed_id = request.POST.get('userId')
        name = request.POST.get('name')
        price = request.POST.get('price')
        price = price[:-1]
        Bed.objects.filter(bed_id=bed_id).update(
            bed_name=name,
            price=price,
        )
        response_data['message'] = '修改成功'
        return JsonResponse(response_data, status=201)
    except Exception as e:
        print(e)
        response_data['message'] = '修改失败'
        return JsonResponse(response_data, status=401)


def get_bed_by_id(request):
    """
    通过id模糊查询用户信息
    :return:
    """
    response_data = {}
    response_data['bed'] = []
    bed_id = request.GET.get('bed_id')
    results = Bed.objects.filter(bed_id=bed_id)
    if results:
        for result in results:
            dict_value = {
                'id': result.bed_id,
                'name': result.bed_name,
                'price': result.price,
            }
    else:
        response_data = {'error': '获取床位信息失败！', 'message': '找不到用户信息.'}
        return JsonResponse(response_data, status=403)
    response_data['bed'] = dict_value
    return JsonResponse(response_data)


def get_bed_by_name(request):
    response_data = {}
    response_data['bed'] = []
    dict_values = {}
    page = request.GET.get('page')
    name = request.GET.get('name')
    try:
        results = Paginator(Bed.objects.filter(bed_name__contains=name), per_page=4).page(page)
        total = Paginator(Bed.objects.filter(bed_name__contains=name), per_page=4).num_pages
        if results:
            for result in results:
                patient_info = Patient.objects.filter(patient_bed_id_id=result.bed_id).first()
                if patient_info:
                    patient_name = patient_info.name
                else:
                    patient_name = '无'
                if result.status == 0:
                    status = '空床'
                else:
                    status = '已入住'
                dict_values[result.bed_id] = {
                    'id': result.bed_id,
                    'name': result.bed_name,
                    'price': result.price,
                    'status': status,
                    'patient_name': patient_name,
                }
        else:
            response_data = {'error': '获取床位信息失败！', 'message': '找不到床位信息.'}
            return JsonResponse(response_data, status=403)
        response_data['bed'] = list(dict_values.values())
        response_data["total"] = total
    except Exception as e:
        print(e)
        response_data = {'error': '获取成为信息失败！', 'message': '找不到床位信息.'}

    return JsonResponse(response_data)