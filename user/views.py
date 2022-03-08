from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
import sys, os
from django.utils import timezone
from django.core.paginator import Paginator
from utils.common import my_login
work_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, work_dir)
from .models import UserTable

patient_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, patient_dir)
from patient.models import Department
from bed.models import Bed
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth


def login(request):
    """
    跳转登录页面
    :param request:
    :return:
    """
    return render(request, 'login.html')


def redirect_new_user(request):
    """
    跳转新增用户页面
    :param request:
    :return:
    """
    info = get_session_info(request)
    return render(request, 'new.html', {'result':info})


@my_login
def main(request):
    result = {}
    username = request.session['username']
    position = request.session['position']
    result['username'] = username
    result['position'] = position
    users = UserTable.objects.all()
    result['user_count'] = len(users)
    result['department_count'] = len(Department.objects.all())
    result['bed0'] = len(Bed.objects.filter(status=0))
    result['bed1'] = len(Bed.objects.filter(status=1))
    try:
        result['bed_available'] ="{:.0f}%" .format(result['bed1']/(result['bed1']+ result['bed0'])*100)
    except Exception as e:
        result['bed_available'] = 0
    return render(request, 'main.html', {'result': result})

@my_login
def index(request):
    info = get_session_info(request)
    return render(request, 'show_user.html',{'result':info})

@my_login
def show(request):
    """
    查询所有用户信息
    :return:
    """
    response_data = {}
    response_data['user'] = []
    dict_values = {}
    page = request.GET.get('page')
    results = Paginator(UserTable.objects.all(), per_page=4).page(page)
    total = Paginator(UserTable.objects.all(), per_page=4).num_pages
    if results:
        for result in results:
            if result.gender == 0:
                sex = '男'
            else:
                sex = '女'
            dict_values[result.user_id] = {
                'id': result.user_id,
                'name': result.name,
                'phone': result.phone,
                'gender': sex,
                'position': result.position,
                'create_time': result.create_time.strftime('%Y-%m-%d %H:%M'),
                'last_modify_time': result.modify_time.strftime('%Y-%m-%d %H:%M')
            }
    else:
        response_data = {'error': '获取用户信息失败！', 'message': '找不到用户信息'}
        return JsonResponse(response_data, status=403)
    response_data['user'] = list(sorted(dict_values.values(), key=lambda item: item['id']))
    response_data["total"] = total
    print(response_data)
    return JsonResponse(response_data)


def get_user_by_name(request):
    """
    通过用户名模糊查询用户信息
    :return:
    """
    response_data = {}
    response_data['user'] = []
    dict_values = {}
    page = request.GET.get('page')
    name = request.GET.get('name')
    try:
        results = Paginator(UserTable.objects.filter(name__contains=name), per_page=4).page(page)
        total = Paginator(UserTable.objects.filter(name__contains=name), per_page=4).num_pages
        if results:
            for result in results:
                if result.gender == 0:
                    sex = '男'
                else:
                    sex = '女'
                dict_values[result.user_id] = {
                    'id': result.user_id,
                    'name': result.name,
                    'phone': result.phone,
                    'gender': sex,
                    'position': result.position,
                    'create_time': result.create_time.strftime('%Y-%m-%d %H:%M'),
                    'last_modify_time': result.modify_time.strftime('%Y-%m-%d %H:%M')
                }
        else:
            response_data = {'error': '获取用户信息失败！', 'message': '找不到用户信息.'}
            return JsonResponse(response_data, status=403)
        response_data['user'] = list(dict_values.values())
        response_data["total"] = total
    except Exception as e:
        print(e)
        response_data = {'error': '获取用户信息失败！', 'message': '找不到用户信息.'}

    return JsonResponse(response_data)


def get_user_by_id(request):
    """
    通过id模糊查询用户信息
    :return:
    """
    response_data = {}
    response_data['user'] = []
    user_id = request.GET.get('id')
    results = UserTable.objects.filter(user_id=user_id)
    if results:
        for result in results:
            if result.gender == 0:
                sex = '男'
            else:
                sex = '女'
            dict_value = {
                'id': result.user_id,
                'name': result.name,
                'phone': result.phone,
                'gender': sex,
                'position': result.position,
            }
    else:
        response_data = {'error': '获取用户信息失败！', 'message': '找不到用户信息.'}
        return JsonResponse(response_data, status=403)
    response_data['user'] = dict_value
    return JsonResponse(response_data)


@csrf_exempt  # 增加装饰器，作用是跳过 csrf 中间件的保护
def add_user(request):
    """
    添加员工
    :return:
    """
    info = get_session_info(request)
    name = request.POST.get('name')
    passwd = request.POST.get('password')
    gender = request.POST.get('gender')
    if gender == '男':
        gender = 0
    else:
        gender = 1
    phone = request.POST.get('phone')
    position = request.POST.get('position')
    description = request.POST.get('description')
    create_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    modify_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    if position == '护士':
        user_role_id = 1
    elif position == '管理员':
        user_role_id = 3
    else:
        user_role_id = 2
    UserTable.objects.create(
        name=name,
        password=passwd,
        gender=gender,
        phone=phone,
        position=position,
        user_role_id=user_role_id,
        description=description,
        create_time=create_time,
        modify_time=modify_time
    )

    return render(request, "show_user.html",{'result':info})


@csrf_exempt
def delete_user(request):
    """
    删除用户信息
    :param user_id: 用户id
    :return:
    """
    user_id = request.POST.get('user_id')
    result = UserTable.objects.filter(user_id=user_id).first()
    try:
        if not result:
            response_data = {'error': '删除用户信息失败！', 'message': '找不到id为%s的用户' % user_id}
            return JsonResponse(response_data, status=403)
        result.delete()
        response_data = {'message': '删除成功！'}
        return JsonResponse(response_data, status=201)
    except Exception as e:
        response_data = {'message': '删除失败！'}
        return JsonResponse(response_data, status=403)


@csrf_exempt
def login_out(request):
    request.session.flush()
    return HttpResponseRedirect('/')

@csrf_exempt
def login_check(request):
    response_data = {}
    name = request.GET.get('name')
    password = request.GET.get('password')
    user = UserTable.objects.filter(name=name, password=password)
    if user:
        # 将用户名存入session中
        request.session["username"] = name
        # print(user.position)
        for i in user:
            request.session['position'] = i.position
        response_data['message'] = '登录成功'
        return JsonResponse(response_data, status=201)
    else:
        return JsonResponse({'message': '用户名或者密码不正确'}, status=401)


@csrf_exempt
def modify_user(request):
    """
    修改用户信息
    :return:
    """
    response_data = {}
    try:
        user_id = request.POST.get('userId')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        position = request.POST.get('position2')
        if gender == '男':
            sex = 0
        else:
            sex = 1
        UserTable.objects.filter(user_id=user_id).update(
            name=name,
            gender=sex,
            phone=phone,
            position=position)
        response_data['message'] = '修改成功'
        return JsonResponse(response_data, status=201)
    except Exception as e:
        print(e)
        response_data['message'] = '修改失败'
        return JsonResponse(response_data,status=401)


def get_session_info(request):
    result = {}
    username = request.session['username']
    position = request.session['position']
    result['username'] = username
    result['position'] = position
    return result
