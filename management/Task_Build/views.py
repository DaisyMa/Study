#coding:utf-8
import sys

from django.conf.global_settings import MEDIA_ROOT
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect

from forms import LoginForm
import logging
import MySQLdb
import xlrd
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.db import connection
from django.db.models import Count
from models import *
from forms import *
from datetime import datetime
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, RequestContext
from django.utils import timezone
import os
from django.db.models import Q
import json
from django.contrib import messages
from django.http import StreamingHttpResponse
import sys

# Create your views here.

# 登录
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = Manager.objects.filter(no=username, email=password)
            if user:
                request.session['username'] = username
                return redirect('/index')
            else:
                user = Staff.objects.filter(no=username, email=password)
                if user:
                    #user=Staff()
                    user=Staff.objects.get(no=username)
                    if user.IsDirector==True:
                        request.session['username'] = username
                        return redirect('/directorTeam')
                    elif user.IsAssistant:
                        request.session['username'] = username
                        return redirect('/assistantTeam')
                    else:
                        request.session['username'] = username
                        return redirect('/staffTeam')
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
        else:
            return render(request, 'failure.html', {'reason': login_form.errors})
    else:
        login_form = LoginForm()
    return render(request, 'login.html', locals())

# 注销
def logout(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])

# 最新项目数据
def index(request):
    list = Project.objects.all()
    list = getPage(request, list)
    if request.method=="POST":
        if request.POST.has_key('filter'):
            filter = request.POST.get('keyword')
            list=Project.objects.filter(Q(name__icontains=filter)|Q(no__icontains=filter))
            list = getPage(request, list)
        else:
            checkbox_list = request.POST.getlist('checkbox_list')
            check_num = len(checkbox_list)
            if checkbox_list:
                for check in checkbox_list:
                    project = Project.objects.get(id=check)
                    project.delete()
                messages.success(request, '已成功删除项目！', extra_tags='alert alert-dismissable alert-info')
                return render(request,'index_m.html', locals())
            else:
                return redirect("http://www.baidu.com")
    return render(request, 'index_m.html', locals())


# 项目详情页
def project(request):
    try:
        id=request.GET.get('id',None)
        try:
            project=Project.objects.get(pk=id)
            return render(request, 'project.html', locals())
        except Project.DoesNotExist:
            return render(request, 'failure.html', {'reason': '没有找到该项目'})
    except:
        return render(request, 'project.html', locals())

#分页代码-通用
def getPage(request,list ):
    paginator = Paginator(list, 5)
    try:
        page = int(request.GET.get('page', 1))
        list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        list = paginator.page(1)
    return list


# 创建项目
def addProject(request):
    if request.method == "POST":
        addProjectForm = AddProjectForm(request.POST)
        loginid=request.session['username']
        deadline=request.POST.get('time')
        time = datetime.now()
        d=time.strftime('%Y%m%d')
        project_latest=Project.objects.latest('id')
        if project_latest:
            count=project_latest.id+1
        else:
            count=1
        if addProjectForm.is_valid():
            Project.objects.create(
                name=addProjectForm.cleaned_data['name'],
                deadline=deadline,
                staffNum=addProjectForm.cleaned_data['staffNum'],
                productNum=addProjectForm.cleaned_data['productNum'],
                content=addProjectForm.cleaned_data['content'],
                manager=Manager.objects.get(no=loginid),
                no="X"+d+str(count)
            )
        project = Project.objects.get(pk=count)
        return render(request, 'project.html', locals())
    else:
        addProjectForm = AddProjectForm()
    return render(request, 'addProject.html', locals())

#编辑项目
def editProject(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    if request.method == "POST":
        form = EditProject(request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return render(request, 'project.html', locals())
        #return redirect('/index')
    else:
        form = EditProject(instance=project)
    return render(request,'editProject.html',{'form': form})

#删除项目
def deleteProject(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    project.delete()
    return redirect('/index')

#导入产品项目
def importProductProList(request):
    list = Project.objects.all()
    list = getPage(request, list)
    return render(request, 'importProductProList.html', locals())

#查看全部项目
def allproject(request):
    try:
        list = Project.objects.all()
        list = getPage(request, list)
    except Exception as e:
        print e
    return render(request, 'allproject.html', locals())

#修改密码
def changepwd(request):
    if request.method == "POST":
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.session['username']
            oldpwd = form.cleaned_data['oldpwd']
            user = Manager.objects.filter(no=username, email=oldpwd)
            if user is not None :
                newpwd1=form.cleaned_data['newpwd1']
                user.set_pwd(newpwd1)
                user.save()
                request.session['username'] = username
                return render(request, 'login.html', locals())
            else:
                user = Staff.objects.filter(no=username, email=oldpwd)
                if user is not None:
                    newpwd1 = form.cleaned_data['newpwd1']
                    user.set_pwd(newpwd1)
                    user.save()
                    request.session['username'] = username
                    return render(request, 'login.html', locals())
                else:
                    return render('changepwd.html',request, 'changepwd.html', locals())
    else:
        form = ChangepwdForm(request.POST)
    return render(request, 'changepwd.html', locals())

#解析Excle文件到数据库
def import_index(request):
    list = Project.objects.all()
    list = getPage(request, list)
    return render(request, 'importStaff.html', locals())

#上传成员文件并解析
def upload_file_staff(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    staffNum=project.staffNum
    staff_exist=Staff.objects.filter(project=project)
    len_staff_exist=len(staff_exist)
    staff_need=staffNum-len_staff_exist
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            uploadFile=ImportFile()
            uploadFile.file=file
            uploadFile.save()
            baseDir = os.path.dirname(os.path.abspath(__name__))
            jpgdir = os.path.join(baseDir, 'upload')

            filename = os.path.join(jpgdir, file.name)
            staff = xlrd.open_workbook(filename)
            sheet = staff.sheet_by_name("sheet1")
            # 建立一个MySQL连接
            database = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="management")
            # 获得游标对象, 用于逐行遍历数据库数据
            cursor = database.cursor()
            # 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题
            rows=sheet.nrows
            if staff_need>0:
                if staff_need>rows:
                    for r in range(1, rows):
                        Staff.objects.create(
                            no=int(sheet.cell(r, 0).value),
                            name=sheet.cell(r, 1).value,
                            sex=sheet.cell(r, 2).value,
                            grade=sheet.cell(r, 3).value,
                            phone=sheet.cell(r, 4).value,
                            email=sheet.cell(r, 5).value,
                            project = project
                        )
                    cursor.close()
                    # 提交
                    database.commit()
                    # 关闭数据库连接
                    database.close()

                    messages.success(request, '已成功导入'+str(rows-1)+'条成员信息！', extra_tags='alert alert-dismissable alert-info')
                    #return HttpResponseRedirect('%s' % next)
                    return render(request, 'upload_file_staff.html',locals())
                else:
                    for r in range(1, staff_need+1):
                        Staff.objects.create(
                            no=int(sheet.cell(r, 0).value),
                            name=sheet.cell(r, 1).value,
                            sex=sheet.cell(r, 2).value,
                            grade=sheet.cell(r, 3).value,
                            phone=sheet.cell(r, 4).value,
                            email=sheet.cell(r, 5).value,
                            project = project
                        )
                    cursor.close()
                    # 提交
                    database.commit()
                    # 关闭数据库连接
                    database.close()
                    messages.success(request, '已成功导入' + str(staff_need) + '条成员信息！',
                                     extra_tags='alert alert-dismissable alert-info')
                return render(request, 'upload_file_staff.html', locals())
            else:
                messages.error(request, '该项目成员已全部导入，不能继续导入！', extra_tags='alert alert-dismissable alert-danger')
                return render(request, 'upload_file_staff.html', locals())
        else:
            form = UploadFileForm()
    else:
        form = UploadFileForm()
    return render(request, 'upload_file_staff.html',locals())

#查看项目成员
def view_member(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    list=Staff.objects.filter(project=project)
    list=getPage(request,list)
    staff_exist = Staff.objects.filter(project=project)
    len_staff_exist = len(staff_exist)
    return render(request,'view_Member.html',locals())

#项目进度
def project_schedule(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    product_exist = Product.objects.filter(project=project)
    deadline=project.deadline
    time = datetime.now()
    now=time.date()
    dayCount=(deadline-now).days
    len_product_exist = len(product_exist)      #已导入产品数
    staff_exist = Staff.objects.filter(project=project)
    len_staff_exist = len(staff_exist)                    #已导入人员数
    task_list=Task.objects.filter(project=project)
    len_task_list=len(task_list)
    task_allot =Task.objects.filter(project=project).filter(IsAllot=True)
    len_task_allot=len(task_allot)
    list=Group.objects.filter(project=project)
    len_list=len(list)
    list=getPage(request,list)
    return render(request,'project_scedule.html',locals())

#上传产品文件并解析
def upload_file_product(request):
        id = request.GET.get('id', None)
        project = Project.objects.get(pk=id)
        productNum = project.productNum
        product_exist = Product.objects.filter(project=project)
        len_product_exist = len(product_exist)
        print len_product_exist
        product_need = productNum - len_product_exist
        print product_need
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                    file = form.cleaned_data['file']
                    uploadFile=ImportFile()
                    uploadFile.file=file
                    uploadFile.save()
                    baseDir = os.path.dirname(os.path.abspath(__name__))
                    jpgdir = os.path.join(baseDir, 'upload')
                    filename = os.path.join(jpgdir, file.name)
                    staff = xlrd.open_workbook(filename)
                    sheet = staff.sheet_by_name("product")
                    database = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="management")
                    cursor = database.cursor()
                    rows=sheet.nrows
                    print rows
                    if product_need>0:
                        if product_need > rows:
                            for r in range(1, rows):
                                product_latest = Product.objects.latest('id')
                                count = product_latest.id + 1
                                # 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题
                                Product.objects.create(
                                    no="C"+str(project.id)+str(count),
                                    name=sheet.cell(r, 0).value,
                                    category=sheet.cell(r, 1).value,
                                    company=sheet.cell(r, 2).value,
                                    project=project,
                                )

                            cursor.close()
                            database.commit()
                            database.close()
                            messages.success(request, '已成功导入' + str(rows-1) + '条产品信息！',
                                             extra_tags='alert alert-dismissable alert-info')
                            return render(request, 'upload_file_product.html', locals())
                        else:
                            for r in range(1, product_need+1):
                                product_latest = Product.objects.latest('id')
                                count = product_latest.id + 1
                                print count
                                # 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题
                                Product.objects.create(
                                    no="C" + str(project.id) + str(count),
                                    name=sheet.cell(r, 0).value,
                                    category=sheet.cell(r, 1).value,
                                    company=sheet.cell(r, 2).value,
                                    project=project,
                                )
                            cursor.close()
                            database.commit()
                            database.close()
                            messages.success(request, '已成功导入' + str(product_need) + '条产品信息！',
                                             extra_tags='alert alert-dismissable alert-info')
                            return render(request, 'upload_file_product.html', locals())
                    else:
                        messages.error(request, '该项目产品已全部导入，不能继续导入！', extra_tags='alert alert-dismissable alert-danger')
            else:
                    form = UploadFileForm()
        else:
                form = UploadFileForm()
        return render(request, 'upload_file_product.html', locals())

#查看项目产品列表
def view_Product(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    product_exist = Product.objects.filter(project=project)
    len_product_exist = len(product_exist)
    list = Product.objects.filter(project=project)
    list = getPage(request, list)
    return render(request,'view_product.html',locals())

#产品列表页
def product(request):
    list = Product.objects.all()
    #product_list = Product.objects.filter(Project=project)
    list = getPage(request,list)
    return render(request, 'product.html', locals())

#所有成员列表
def staff(request):
    list = Staff.objects.all()
   # staff_list = Product.objects.filter(Project=project)
    list = getPage(request,list)
    return render(request, 'staff.html', locals())

#设置小组的项目列表
def setGroupList(request):
    list = Project.objects.all()
    list = getPage(request, list)
    return render(request, 'setGroupList.html', locals())

#添加小组
def addGroup(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    group_list=Group.objects.filter(project=project)
    projectStaff=project.staffNum
    list = Group.objects.filter(project=project)
    list = getPage(request, list)
    len=0
    if request.method == "POST":
            for group in group_list:
                staNum = group.staffNum
                len = len + staNum
            form=AddGroup(request.POST)
            group_latest = Group.objects.latest('id')
            count = group_latest.id + 1
            projectNeed=projectStaff-len
            if form.is_valid():
                staffNum = form.cleaned_data['staffnum']
                if staffNum > projectNeed:
                    messages.error(request, '小组人数大于项目所需人数，请重新输入小组人数！', extra_tags='alert alert-dismissable alert-danger')
                    return render(request, 'addGroup.html', locals())
                else:
                    Group.objects.create(
                        no="Z" + str(project.id) + str(count),
                        name=form.cleaned_data['groupname'],
                        staffNum = form.cleaned_data['staffnum'],
                        project=project
                    )
                group_latest = Group.objects.latest('id')
                messages.success(request, '已成功创建小组，小组编号为' + str(group_latest),
                                     extra_tags='alert alert-dismissable alert-info')
                return render(request, 'addGroup.html', locals())
    else:
        form = AddGroup(request.POST)
    return render(request, 'addGroup.html', locals())

#项目的小组列表
def viewGroup(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    list=Group.objects.filter(project=project)
    list = getPage(request, list)
    return render(request,'viewGroup.html',locals())

#设置小组列表
def setMember(request):
    list = Project.objects.all()
    list = getPage(request, list)
    return render(request, 'setMember.html', locals())

#添加组员界面查看小组列表
def setMember_viewGroup(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    list=Group.objects.filter(project=project)
    list = getPage(request, list)
    return render(request,'setmember_viewgroup.html',locals())

#添加组员
def choiceMember(request):
    id = request.GET.get('id', None)
    group=Group.objects.get(pk=id)
    project=group.project
    list=Staff.objects.filter(project=project).filter(group__isnull=True)
    list=getPage(request, list)
    staff_group=Staff.objects.filter(group=group)
    staff_group_num=len(staff_group)   #小组中已存在的人数
    print staff_group_num
    groupNum=group.staffNum            #小组需求人数
    print groupNum
    group_need=groupNum-staff_group_num  #小组需导入人数
    print group_need

    if request.method=="POST":
            checkbox_list=request.POST.getlist('checkbox_list')
            check_num=len(checkbox_list)
            print check_num
            if group_need>0:

                    if check_num > group_need:
                        messages.error(request, '选择人数大于需导入小组人数，请重新选择！',
                                       extra_tags='alert alert-dismissable alert-danger')
                        return render(request, 'choicemember.html', locals())
                    else:
                                for check in checkbox_list:
                                    staff=Staff.objects.get(id=check)
                                    print staff
                                    staff.group=group
                                    staff.save()
                                messages.success(request, '已成功导入'+ str(check_num) +'位组员！', extra_tags='alert alert-dismissable alert-info')
                                return render(request, 'choicemember.html', locals())
            else:
                messages.error(request, '该小组成员已全部添加，继续添加将超出小组人数！', extra_tags='alert alert-dismissable alert-danger')
                return render(request, 'choicemember.html', locals())
    else:
        return render(request,'choicemember.html',locals())

#查看项目的成员列表
def viewMember(request):
    id = request.GET.get('id', None)
    group = Group.objects.get(pk=id)
    project=group.project
    list=Staff.objects.filter(group=id)
    list=getPage(request, list)
    return render(request,"viewmember.html",locals())

#需分配的项目列表
def allotList(request):
    loginid = request.session['username']
    manager=Manager.objects.get(no=loginid)
    list = Project.objects.filter(manager=manager)
    list = getPage(request, list)
    return render(request, 'allotlist.html', locals())

#分配到小组的项目列表
def allotGroup(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    list = Group.objects.filter(project=project)
    list = getPage(request, list)
    return render(request, 'allotgroup.html', locals())

#设置主管
def setDirector(request):
    id = request.GET.get('id', None)
    group = Group.objects.get(pk=id)
    project = group.project
    list = Staff.objects.filter(group=id)
    list = getPage(request, list)
    if request.method == "POST":
        radio = request.POST.getlist('radio')
        if radio:
            for radio in radio:
                staff = Staff.objects.get(id=radio)
                if staff.IsAssistant:
                    messages.error(request, '该成员为主管助理，请重新选择！', extra_tags='alert alert-dismissable alert-danger')
                    return render(request, 'setdirector.html', locals())
                else:
                    staff.IsDirector = True
                    staff.save()
                    group.directorNo=staff.no
                    group.save()
                    messages.success(request, '已成功设置为主管！',
                                     extra_tags='alert alert-dismissable alert-info')
                    return render(request, 'setdirector.html', locals())
            return render(request, 'setdirector.html', locals())
    return render(request, "setdirector.html", locals())


#设置助理
def setAssistant(request):
    id = request.GET.get('id', None)
    group = Group.objects.get(pk=id)
    project = group.project
    list = Staff.objects.filter(group=id)
    list = getPage(request, list)
    if request.method == "POST":
        radio = request.POST.getlist('radio')
        if radio:
            for radio in radio:
                staff = Staff.objects.get(id=radio)
                if staff.IsDirector:
                    messages.error(request, '该成员为小组主管，请重新选择！', extra_tags='alert alert-dismissable alert-danger')
                    return render(request, 'setassistant.html', locals())
                else:
                    staff.IsAssistant = True
                    staff.save()
                    group.assistantNo=staff.no
                    group.save()
                    messages.success(request, '已成功设置为小组助理！',
                                     extra_tags='alert alert-dismissable alert-info')
                    return render(request, 'setassistant.html', locals())
            return render(request, 'setassistant.html', locals())
    return render(request, "setassistant.html", locals())

#创建任务的项目列表
def addTask_list(request):
    try:
        loginid = request.session['username']
        manager=Manager.objects.get(no=loginid)
        list = Project.objects.filter(manager=manager)
        list = getPage(request, list)
    except Exception as e:
        print e
    return render(request, 'addtaskprolist.html', locals())

#选择产品
def choiceProduct(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    list=Product.objects.filter(project=project).filter(task__isnull=True).filter(subTask__isnull=True)
    list = getPage(request, list)
    if request.method == "POST":
        checkbox_list = request.POST.getlist('checkbox_list')
        check_num = len(checkbox_list)
        if checkbox_list:
            task_latest = Task.objects.latest('id')
            count = task_latest.id + 1
            Task.objects.create(
                no="R" + str(project.id) + str(count),
                productNum=check_num,
                project=project,
            )
            task_latest = Task.objects.latest('id')
            for check in checkbox_list:
                product = Product.objects.get(id=check)
                product.task = task_latest
                product.save()
            messages.success(request, '已成功创建任务，任务编号为'+str(task_latest.no),extra_tags='alert alert-dismissable alert-info')
           # task_latest = taskDetail(request,task_latest)
            return render(request, 'choiceproduct.html', locals())
    else:
        return render(request, 'choiceproduct.html', locals())

#任务详情页
def taskDetail(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    list=Product.objects.filter(task=task)
    list = getPage(request, list)
    return render(request, 'taskdetail.html', locals())

#分配任务项目列表
def allotTaskList(request):
    try:
        loginid = request.session['username']
        manager = Manager.objects.get(no=loginid)
        list = Project.objects.filter(manager=manager)
        list = getPage(request, list)
    except Exception as e:
        print e
    return render(request, 'allottasklist.html', locals())

#任务列表
def taskList(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    list=Task.objects.filter(project=project)
    list=getPage(request, list)
    return render(request,'allottask_grouplist.html',locals())

#将任务分配到小组
def allotToGroup(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    project = task.project
    list = Group.objects.filter(project=project)
    list = getPage(request, list)
    if request.method == "POST":
        radio = request.POST.getlist('radio')
        if radio:
            for radio in radio:
                group = Group.objects.get(id=radio)
                task.group = group
                task.IsAllot=True
                task.IsGroupTask=True
                task.allotTime = datetime.now()
                task.deadline=project.deadline
                task.save()
                messages.success(request, '已成功分配到小组'+str(group.no) ,
                             extra_tags='alert alert-dismissable alert-info')
            return render(request, 'allotToGroup.html', locals())
        else:
            return redirect("http://www.baidu.com")
    else:
        return render(request, 'allotToGroup.html', locals())

#将任务分配到个人
def allotToStaff(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    project = task.project
    list = Staff.objects.filter(project=project)
    list = getPage(request, list)
    if request.method == "POST":
        radio = request.POST.getlist('radio')
        if radio:
            for radio in radio:
                staff = Staff.objects.get(id=radio)
                task.IsAllot=True
                task.staff = staff
                task.group = staff.group
                task.deadline = project.deadline
                task.allotTime=datetime.now()
                task.IsGroupTask=False
                task.save()
            messages.success(request, '已成功分配到成员' + str(staff.no),
                                 extra_tags='alert alert-dismissable alert-info')
            return render(request, 'allotToStaff.html', locals())
    return render(request, "allotToStaff.html", locals())

def test(request):
    project_list = Project.objects.all()
    project_list = getPage(request, project_list)

    return render(request,"test.html",locals())

#查看任务项目列表
def viewTask_ProjectList(request):
    loginid = request.session['username']
    manager = Manager.objects.get(no=loginid)
    list = Project.objects.filter(manager=manager)
    list = getPage(request, list)
    return render(request,'viewTask_ProjectList.html',locals())

def viewTask(request):
    id = request.GET.get('id', None)
    project = Project.objects.get(pk=id)
    task_list_notAllot = Task.objects.filter(project=project).filter(IsAllot=False)
    len_notAllot=len(task_list_notAllot)
    task_list_notAllot = getPage(request,  task_list_notAllot)
    task_list_allot=Task.objects.filter(project=project).filter(IsAllot=True)
    task_list_allot = getPage(request, task_list_allot)
    len_allot=len(task_list_allot)
    return render(request, 'viewTask.html', locals())

#获取主管组织概况
def directorTeam(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    group=staff.group
    project=staff.project
    list=Staff.objects.filter(group=group)
    #staff_list = getPage(request, staff_list)
    assistant=list.get(IsAssistant=True)
    manager=project.manager
    return render(request,'directorTeam.html',locals())

#获取小组任务
def groupTask(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    group = staff.group
    project = staff.project
    list = Task.objects.filter(group=group)
    list=getPage(request,list)
    #task_list_allot=Task.objects.filter(group=group).filter(IsReallot=True)
    return render(request,'groupTask.html',locals())

#选择产品创建子任务
def subTask_choiceProduct(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    project = task.project
    list=Product.objects.filter(task=task).filter(subTask__isnull=True)
    list = getPage(request, list)
    if request.method == "POST":
        checkbox_list = request.POST.getlist('checkbox_list')
        check_num = len(checkbox_list)
        if checkbox_list:
            subtask_latest = SubTask.objects.latest('id')
            count = subtask_latest.id + 1
            SubTask.objects.create(
                no="S" + str(task.no) + str(count),
                productNum=check_num,
                task=task,
            )
            task.IsReallot=True   #更新任务表格是否分配的属性
            task.save()
            subtask_latest = SubTask.objects.latest('id')
            for check in checkbox_list:
                product = Product.objects.get(id=check)
                product.subTask = subtask_latest
                product.save()
            return render(request, 'subTask_choiceProduct.html', locals())

    else:
        return render(request, 'subTask_choiceProduct.html', locals())

#主管所在组被分配的任务列表
def groupTaskList(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    project=staff.project
    group = staff.group
    list=Task.objects.filter(group=group)
    list = getPage(request, list)
    return render(request,'groupTaskList.html',locals())

#选择需分配的子任务
def choiceSubTask(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    list=SubTask.objects.filter(task=task).filter(IsAllot=False)
    list=getPage(request,list)
    return render(request,'choiceSubTask.html',locals())

#选择组员分配子任务
def subTask_choiceMember(request):
    id = request.GET.get('id', None)
    subtask = SubTask.objects.get(pk=id)
    task=subtask.task
    project=task.project
    group=task.group
    list=Staff.objects.filter(group=group)
    list = getPage(request, list)
    if request.method == "POST":
            radio = request.POST.getlist('radio')
            if radio:
                for radio in radio:
                    staff = Staff.objects.get(id=radio)
                    subtask.IsAllot = True
                    subtask.staff = staff
                    subtask.allotTime = datetime.now()
                    subtask.save()
                messages.success(request, '已成功分配子任务',
                                     extra_tags='alert alert-dismissable alert-info')
            return render(request, 'subTask_choiceMember.html', locals())
    return render(request, "subTask_choiceMember.html", locals())

#获取个人任务
def staffTask_staff(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    list = Task.objects.filter(staff=staff)
    list = getPage(request, list)
    if request.method == "POST":
            c = request.POST['radio']
            if c =='task':
                return redirect('/staffTask_staff')
            else :
                return redirect('/staffTask_group')
    return render(request, 'staffTask_staff.html', locals())

#个人任务详情
def staffTask_staff_detail(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    list=Product.objects.filter(task=task)
    list=getPage(request,list)
    return render(request,'staffTask_staff_detail.html',locals())

#上传文件-产品文件上传情况
def staffTask_staff_productFile(request):
    id = request.GET.get('id', None)
    product = Product.objects.get(pk=id)
    task = product.task
    rateFile_len=len(RateFile.objects.filter(product=product))
    if rateFile_len > 0:
        rateFile=RateFile.objects.get(product=product)
    else:
        rateFile=0
    clauseFile_len = len(ClauseFile.objects.filter(product=product))
    if clauseFile_len>0:
        clauseFile=ClauseFile.objects.get(product=product)
    else:
        clauseFile=0
    cashFile_len=len(CashFile.objects.filter(product=product))
    if cashFile_len > 0:
        cashFile = CashFile.objects.get(product=product)
    else:
        cashFile = 0
    return render(request,'staffTask_staff_productFile.html',locals())


#上传产品费率文件
def rateFile_upload(request):
    id = request.GET.get('id', None)
    product = Product.objects.get(pk=id)
    task = product.task
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    if request.method=="POST":
        form = UploadFileInfo(request.POST, request.FILES)
        if form.is_valid():                                   #提交验证未做（是否已提交），提交后返回界面
            pageNum = form.cleaned_data['pageNum']
            fileNote = form.cleaned_data['filenote']
            file = form.cleaned_data['file']
            name=file.name
            print name
            rateFile_len = len(RateFile.objects.filter(product=product))
            if rateFile_len > 0:
                rateFile = RateFile.objects.get(product=product)
                if rateFile.IsSubmit:
                    messages.error(request, '该产品的费率文件已提交，不能继续上传！', extra_tags='alert alert-dismissable alert-danger')
                else:
                    rateFile.delete()
                    RateFile.objects.create(
                        no="WF" + str(product.no),
                        name=name,
                        #name=product.name,
                        file=file,
                        pageNum=pageNum,
                        fileNote=fileNote,
                        product=Product.objects.get(pk=id),
                        staff=staff,
                    )
                    messages.success(request, '文件已覆盖上传！', extra_tags='alert alert-dismissable alert-info')
            else:
                RateFile.objects.create(
                    no = "WF" + str(product.no),
                    name = name,
                    file = file,
                    pageNum = pageNum,
                    fileNote = fileNote,
                    product=Product.objects.get(pk=id),
                    staff=staff,
                )
                messages.success(request, '文件已成功上传！', extra_tags='alert alert-dismissable alert-info')
    else:
        form = UploadFileInfo(request.POST, request.FILES)
    return render(request,'rateFile_upload.html',locals())

#上传产品条款文件
def clauseFile_upload(request):
    id = request.GET.get('id', None)
    product = Product.objects.get(pk=id)
    task = product.task
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    if request.method=="POST":
        form = UploadFileInfo(request.POST, request.FILES)
        if form.is_valid():                                   #提交验证未做（是否已提交），提交后返回界面
            pageNum = form.cleaned_data['pageNum']
            fileNote = form.cleaned_data['filenote']
            file = form.cleaned_data['file']
            name = file.name
            clauseFile_len = len(ClauseFile.objects.filter(product=product))
            if clauseFile_len > 0:
                clauseFile = ClauseFile.objects.get(product=product)
                if clauseFile.IsSubmit:
                    messages.error(request, '该产品的条款文件已提交，不能继续上传！', extra_tags='alert alert-dismissable alert-danger')
                else:
                    clauseFile.delete()
                    ClauseFile.objects.create(
                        no="WT" + str(product.no),
                        name=name,
                        file=file,
                        pageNum=pageNum,
                        fileNote=fileNote,
                        product=Product.objects.get(pk=id),
                        staff=staff,
                    )
                    messages.success(request, '文件已覆盖上传！', extra_tags='alert alert-dismissable alert-info')
            else:
                ClauseFile.objects.create(
                    no = "WT" + str(product.no),
                    name = name,
                    file = file,
                    pageNum = pageNum,
                    fileNote = fileNote,
                    product=Product.objects.get(pk=id),
                    staff=staff,
                )
                messages.success(request, '文件已成功上传！', extra_tags='alert alert-dismissable alert-info')
    else:
        form = UploadFileInfo(request.POST, request.FILES)
    return render(request,'clauseFile_upload.html',locals())

#上传产品现金价值表
def cashFile_upload(request):
    id = request.GET.get('id', None)
    product = Product.objects.get(pk=id)
    task = product.task
    loginid = request.session['username']
    staff=Staff.objects.get(no=loginid)
    #staff = Staff.objects.get(no=loginid)
    if request.method=="POST":
        form = UploadFileInfo(request.POST, request.FILES)
        if form.is_valid():                                   #提交验证未做（是否已提交），提交后返回界面
            pageNum = form.cleaned_data['pageNum']
            fileNote = form.cleaned_data['filenote']
            file = form.cleaned_data['file']
            cashFile_len = len(CashFile.objects.filter(product=product))
            if cashFile_len > 0:
                cashFile = CashFile.objects.get(product=product)
                if cashFile.IsSubmit:
                    messages.error(request, '该产品的现金价值表已提交，不能继续上传！', extra_tags='alert alert-dismissable alert-danger')
                else:
                    cashFile.delete()
                    CashFile.objects.create(
                        no="WX" + str(product.no),
                        name=product.name,
                        file=file,
                        pageNum=pageNum,
                        fileNote=fileNote,
                        product=Product.objects.get(pk=id),
                        staff=Staff.objects.get(no=loginid),
                    )
                    messages.success(request, '文件已覆盖上传！', extra_tags='alert alert-dismissable alert-info')
            else:
                CashFile.objects.create(
                    no = "WX" + str(product.no),
                    name = product.name,
                    file = file,
                    pageNum = pageNum,
                    fileNote = fileNote,
                    product=Product.objects.get(pk=id),
                    staff=Staff.objects.get(no=loginid),
                )
                messages.success(request, '文件已成功上传！', extra_tags='alert alert-dismissable alert-info')
    else:
        form = UploadFileInfo(request.POST, request.FILES)
    return render(request,'cashFile_upload.html',locals())



#获取小组任务
def staffTask_group(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    list = SubTask.objects.filter(staff=staff)
    list = getPage(request, list)
    if request.method == "POST":
        c = request.POST['radio']
        if c == 'task':
            return redirect('/staffTask_staff')
        else:
            return redirect('/staffTask_group')
    return render(request, 'staffTask_group.html', locals())

#小组任务详情
def staffTask_group_detail(request):
    id = request.GET.get('id', None)
    subtask = SubTask.objects.get(pk=id)
    task=subtask.task
    list=Product.objects.filter(subTask=subtask)
    list=getPage(request,list)
    return render(request,'staffTask_group_detail.html',locals())

#选择产品上传文件
def staffTask_group_upload(request):
    id = request.GET.get('id', None)
    product = Product.objects.get(pk=id)
    subTask=product.subTask
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    if request.method=="POST":
        form = UploadFileInfo(request.POST, request.FILES)
        c = request.POST['radio']
        if form.is_valid():                                   #提交验证未做（是否已提交），提交后返回界面
           # radio=form.fields['fileCategory'].choices
            pageNum = form.cleaned_data['pageNum']
            fileNote = form.cleaned_data['filenote']
            file = form.cleaned_data['file']
            if c=='rate':
                RateFile.objects.create(
                    no = "WF" + str(product.no),
                    name = product.name,
                    file = file,
                    pageNum = pageNum,
                    fileNote = fileNote,
                    product=product,
                    staff=staff,
                )

            elif c=='clause':
                ClauseFile.objects.create(
                    no="WT" + str(product.no),
                    name = product.name,
                    file = file,
                    pageNum = pageNum,
                    fileNote = fileNote,
                    product=Product.objects.get(pk=id),
                    staff=staff,
                )
            else:
                CashFile.objects.create(
                    no = "WX" + str(product.no),
                    name = product.name,
                    file = file,
                    pageNum = pageNum,
                    fileNote = fileNote,
                    product=Product.objects.get(pk=id),
                    staff=staff,
                )
            print product
        else:
            form = UploadFileInfo()
    else:
        form = UploadFileInfo()
    return render(request,'staffTask_group_upload.html',locals())

#主管文件查看
def director_selectFile(request):
    c = request.POST['radio']
    print c
    return render(request,'director_select_File.html',locals())

#提交费率文件
def manageFile_d(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    list=RateFile.objects.filter(staff=staff)
    list = getPage(request, list)
    len_upload=len(list)
    submitlist=RateFile.objects.filter(staff=staff).filter(IsSubmit=True)
    len_submit=len(submitlist)
    upload_ratefile=RateFile.objects.filter(staff=staff)

    if request.method == "POST":
        if request.POST.has_key('filter'):
            c = request.POST['radio']
            if c == 'rate':
                return redirect('/manageFile_d')
            elif c == 'clause':
                return redirect('/manageFile_d_clause')
            else:
                return redirect('manageFile_d_cash')
        else:
            checkbox_list = request.POST.getlist('checkbox_list')
            if checkbox_list:
                for check in checkbox_list:
                    file = RateFile.objects.get(id=check)
                    print file
                    file.IsSubmit = True
                    submitTime = timezone.now()
                    file.save()
                messages.success(request, '提交成功！',extra_tags='alert alert-dismissable alert-info')
                return render(request,'manageFile_d.html',locals())
            else:
                messages.error(request, '未选中任何文件，请选择！', extra_tags='alert alert-dismissable alert-danger')
                return render(request, 'manageFile_d.html', locals())
    return render(request,'manageFile_d.html',locals())

#提交条款文件
def manageFile_d_clause(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    list = ClauseFile.objects.filter(staff=staff)
    list = getPage(request, list)
    len_upload = len(list)
    submitlist = ClauseFile.objects.filter(staff=staff).filter(IsSubmit=True)
    len_submit = len(submitlist)
    if request.method == "POST":
        if request.POST.has_key('filter'):
            c = request.POST['radio']
            if c == 'rate':
                return redirect('/manageFile_d')
            elif c == 'clause':
                return redirect('/manageFile_d_clause')
            else:
                return redirect('manageFile_d_cash')
        else:
            checkbox_list = request.POST.getlist('checkbox_list')
            if checkbox_list:
                for check in checkbox_list:
                    file = ClauseFile.objects.get(id=check)
                    file.IsSubmit = True
                    submitTime = timezone.now()
                    file.save()
                    messages.success(request, '提交成功！', extra_tags='alert alert-dismissable alert-info')
                return render(request, 'manageFile_d_clause.html', locals())
            else:
                messages.error(request, '未选中任何文件，请选择！', extra_tags='alert alert-dismissable alert-danger')
                return render(request, 'manageFile_d_clause.html', locals())
    return render(request, 'manageFile_d_clause.html', locals())

#提交现金价值表文件
def manageFile_d_cash(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    list = CashFile.objects.filter(staff=staff)
    list = getPage(request, list)
    len_upload = len(list)
    submitlist = CashFile.objects.filter(staff=staff).filter(IsSubmit=True)
    len_submit = len(submitlist)
    if request.method == "POST":
        if request.POST.has_key('filter'):
            c = request.POST['radio']
            if c == 'rate':
                return redirect('/manageFile_d')
            elif c == 'clause':
                return redirect('/manageFile_d_clause')
            else:
                return redirect('manageFile_d_cash')
        else:
            checkbox_list = request.POST.getlist('checkbox_list')
            len_list=len(checkbox_list)
            if checkbox_list:
                for check in checkbox_list:
                    file = CashFile.objects.get(id=check)
                    file.IsSubmit = True
                    submitTime=timezone.now()
                    file.save()
                    messages.success(request, '已成功提交+'+len_list+'条文件！', extra_tags='alert alert-dismissable alert-info')
                return render(request, 'manageFile_d_cash.html', locals())
            else:
                messages.error(request, '未选中任何文件，请选择！', extra_tags='alert alert-dismissable alert-danger')
                return render(request, 'manageFile_d_cash.html', locals())
    return render(request, 'manageFile_d_cash.html', locals())

#审核经理分配到组员的任务列表
def check_staffTask(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    group=staff.group #获取组号
    list=Task.objects.filter(group=group).filter(IsGroupTask=False) #查出本小组且为经理直接分配到个人的任务
    list=getPage(request,list )
    if request.method == "POST":
        c = request.POST['radio']
        if c == 'task':
            return redirect('/check_staffTask')
        else:
            return redirect('/check_groupTask')
    return render(request, 'check_staffTask.html', locals())

#审核个人任务详情
def check_staffTask_detail(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    list = Product.objects.filter(task=task)
    list = getPage(request, list)
    return render(request,'check_staffTask_detail.html',locals())

#审核经理分配到小组的任务
def check_groupTask(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    group = staff.group
    list=Task.objects.filter(group=group).filter(IsGroupTask=True)
    list = getPage(request, list)
    if request.method == "POST":
        c = request.POST['radio']
        if c == 'task':
            return redirect('/check_staffTask')
        else:
            return redirect('/check_groupTask')
    return render(request,'check_groupTask.html',locals())


#初审产品的文件提交情况
def checkProductFile(request):
    id = request.GET.get('id', None)
    product = Product.objects.get(pk=id)
    task = product.task
    rateFile_len = len(RateFile.objects.filter(product=product))
    if rateFile_len > 0:
        rateFile = RateFile.objects.get(product=product)
    else:
        rateFile = 0
    clauseFile_len = len(ClauseFile.objects.filter(product=product))
    if clauseFile_len > 0:
        clauseFile = ClauseFile.objects.get(product=product)
    else:
        clauseFile = 0
    cashFile_len = len(CashFile.objects.filter(product=product))
    if cashFile_len > 0:
        cashFile = CashFile.objects.get(product=product)
    else:
        cashFile = 0
    return render(request,'check_ProductFile.html',locals())

#下载费率文件
def load_rateFile(request):
       id = request.GET.get('id', None)
       file = RateFile.objects.get(pk=id)
       baseDir = os.path.dirname(os.path.abspath(__name__))
       jpgdir = os.path.join(baseDir, 'upload')
       filename = os.path.join(jpgdir, file.name)
       staff=file.staff
       no=staff.no
       product=file.product
       #name=product.name
       def file_iterator(filename, chunk_size=512):
           with open(filename) as f:
               while True:
                   c = f.read(chunk_size)
                   if c:
                       yield c
                   else:
                       break
       response = StreamingHttpResponse(file_iterator(filename))
       response['Content-Type'] = 'application/octet-stream'
       response['Content-Disposition'] = 'attachment;filename="{0}"'.format("ratefile"+"_"+file.name)
       #response['Content-Disposition'] = 'attachment;filename='file.name.encode('utf-8')+filetype_.encode('utf-8')
      # response['Content-Disposition'] = 'attachment; filename=' + filename_.encode('utf-8') + filetype_.encode('utf-8')  # 设定传输给客户端的文件名称
        # 传输给客户端的文件大小
       return response


#下载条款文件
def load_clauseFile(request):
    id = request.GET.get('id', None)
    file = ClauseFile.objects.get(pk=id)
    baseDir = os.path.dirname(os.path.abspath(__name__))
    jpgdir = os.path.join(baseDir, 'upload')
    filename = os.path.join(jpgdir, file.name)
    staff = file.staff
    no = staff.no
    product = file.product
    #name = product.name

    def file_iterator(filename, chunk_size=512):
        with open(filename) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    #response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
        "clause" + "_" + file.name)
    return response

#下载现金价值表
def load_cashFile(request):
    id = request.GET.get('id', None)
    file = CashFile.objects.get(pk=id)
    baseDir = os.path.dirname(os.path.abspath(__name__))
    jpgdir = os.path.join(baseDir, 'upload')
    filename = os.path.join(jpgdir, file.name)
    staff = file.staff
    no = staff.no
    product = file.product
    #name = product.name

    def file_iterator(filename, chunk_size=512):
        with open(filename) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}".format(name.encode("utf8"))'.format("cashfile"+file.name+"_"+no)
    return response

#审核费率文件
def check_rateFile(request):
    id = request.GET.get('id', None)
    file = RateFile.objects.get(pk=id)
    staff=file.staff
    name=staff.name
    if request.method == "POST":
        if request.POST.has_key('check'):
            checkbox_company = request.POST.getlist('IsCompany')
            if checkbox_company:
                file.IsCompany=True
            checkbox_product = request.POST.getlist('IsProduct')
            if checkbox_product:
                file.IsProduct=True
            checkbox_page = request.POST.getlist('IsPage')
            if checkbox_page:
                file.IsPage=True
            checkbox_category = request.POST.getlist('IsCategory')
            if checkbox_category:
                file.IsPage=True
            file.IsCheck=True
            file.checkTime=timezone.now()
            file.IsCheckPass=True
            file.save()
            messages.success(request, '文件已审核通过！', extra_tags='alert alert-dismissable alert-info')
        else:
            file.delete()
            messages.success(request, '文件已退回，提交人可重新提交！', extra_tags='alert alert-dismissable alert-info')
    else:

        return render(request,'check_rateFile.html',locals())
    return render(request, 'check_rateFile.html', locals())

#审核条款文件
def check_clauseFile(request):
    id = request.GET.get('id', None)
    file = ClauseFile.objects.get(pk=id)
    staff=file.staff
    product=file.product
    pro_name=product.name
    name=staff.name
    if request.method == "POST":
        if request.POST.has_key('check'):
            checkbox_company = request.POST.getlist('IsCompany')
            if checkbox_company:
                file.IsCompany=True
            checkbox_product = request.POST.getlist('IsProduct')
            if checkbox_product:
                file.IsProduct=True
            checkbox_page = request.POST.getlist('IsPage')
            if checkbox_page:
                file.IsPage=True
            checkbox_category = request.POST.getlist('IsCategory')
            if checkbox_category:
                file.IsPage=True
            file.IsCheck=True
            file.checkTime=timezone.now()
            file.IsCheckPass=True
            file.save()
            messages.success(request, '文件已审核通过！', extra_tags='alert alert-dismissable alert-info')
        else:
            file.delete()
            messages.success(request, '文件已退回，提交人可重新提交！', extra_tags='alert alert-dismissable alert-info')
    else:

        return render(request,'check_clausefile.html',locals())
    return render(request, 'check_clausefile.html', locals())

#审核现金价值表
def check_cashFile(request):
    id = request.GET.get('id', None)
    file =CashFile.objects.get(pk=id)
    staff=file.staff
    name=staff.name
    if request.method == "POST":
        if request.POST.has_key('check'):
            checkbox_company = request.POST.getlist('IsCompany')
            if checkbox_company:
                file.IsCompany=True
            checkbox_product = request.POST.getlist('IsProduct')
            if checkbox_product:
                file.IsProduct=True
            checkbox_page = request.POST.getlist('IsPage')
            if checkbox_page:
                file.IsPage=True
            checkbox_category = request.POST.getlist('IsCategory')
            if checkbox_category:
                file.IsPage=True
            file.IsCheck=True
            file.checkTime=timezone.now()
            file.IsCheckPass=True
            file.save()
            messages.success(request, '文件已审核通过！', extra_tags='alert alert-dismissable alert-info')
        else:
            file.delete()
            messages.success(request, '文件已退回，提交人可重新提交！', extra_tags='alert alert-dismissable alert-info')
    else:

        return render(request,'check_cashfie.html',locals())
    return render(request, 'check_cashfie.html', locals())

#查看小组任务的子任务列表
def check_groupTask_subtask(request):
    id = request.GET.get('id', None)
    task =Task.objects.get(pk=id)
    list=SubTask.objects.filter(task=task)
    list= getPage(request, list)
    return render(request,'check_groupTask_subtask.html',locals())

#查看各子任务的产品列表
def check_subTask_product(request):
    id = request.GET.get('id', None)
    task = SubTask.objects.get(pk=id)
    list=Product.objects.filter(subTask=task)
    list = getPage(request, list)
    return render(request,'check_groupTask_detail.html',locals())

#经理审核分配的所有个人任务
def review_staffTask(request):
    loginid = request.session['username']
    manager = Manager.objects.get(no=loginid)
    list=Task.objects.filter(IsGroupTask=False).filter(IsAllot=True).order_by('-allotTime') #查出本小组且为经理直接分配到个人的任务
    list=getPage(request,list )
    if request.method == "POST":
        c = request.POST['radio']
        if c == 'task':
            return redirect('/review_staffTask')
        else:
            return redirect('/review_groupTask')
    return render(request, 'review_staffTask.html', locals())

#经理审核分配到小组的任务
def review_groupTask(request):
    loginid = request.session['username']
    manager = Manager.objects.get(no=loginid)
    list = Task.objects.filter(IsGroupTask=True).filter(IsAllot=True).order_by('-allotTime')  # 查出本小组且为经理直接分配到个人的任务
    list = getPage(request, list)
    if request.method == "POST":
        c = request.POST['radio']
        if c == 'task':
            return redirect('/review_staffTask')
        else:
            return redirect('/review_groupTask')
    else:
        return render(request, 'review_groupTask.html', locals())

#复审文件，小组任务下的子任务列表
def review_grouptask_subtask(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    list = SubTask.objects.filter(task=task)
    list = getPage(request, list)
    return render(request, 'review_grouptask_subtask.html', locals())

#复审文件，子任务下的产品列表
def review_subtask_product(request):
    id = request.GET.get('id', None)
    task = SubTask.objects.get(pk=id)
    list = Product.objects.filter(subTask=task)
    list = getPage(request, list)
    return render(request,'review_subtask_product.html',locals())

#复审文件，产品的文件上传、提交、初审情况
def review_product_file(request):
    id = request.GET.get('id', None)
    product = Product.objects.get(pk=id)
    task = product.task
    rateFile_len = len(RateFile.objects.filter(product=product))
    if rateFile_len > 0:
        rateFile = RateFile.objects.get(product=product)
    else:
        rateFile = 0
    clauseFile_len = len(ClauseFile.objects.filter(product=product))
    if clauseFile_len > 0:
        clauseFile = ClauseFile.objects.get(product=product)
    else:
        clauseFile = 0
    cashFile_len = len(CashFile.objects.filter(product=product))
    if cashFile_len > 0:
        cashFile = CashFile.objects.get(product=product)
    else:
        cashFile = 0
    return render(request,'review_productfile.html',locals())

#复审文件、个人任务详情
def review_stafftask_detail(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    list = Product.objects.filter(task=task)
    list = getPage(request, list)
    return render(request, 'review_staffTask_detail.html', locals())

#复审费率文件
def review_ratefile(request):
    id = request.GET.get('id', None)
    file = RateFile.objects.get(pk=id)
    staff=file.staff
    group=staff.group
    directorno=group.directorNo
    assistantno=group.assistantNo
    director=Staff.objects.get(no=directorno)
    assistant=Staff.objects.get(no=assistantno)
    if director==staff:
        check=assistant
    else:
        check=director
    product = file.product
    pro_name = product.name
    name = staff.name
    if request.method == "POST":
        if request.POST.has_key('check'):
            checkbox_company = request.POST.getlist('IsCompany')
            if checkbox_company:
                file.IsCompany = True
            checkbox_product = request.POST.getlist('IsProduct')
            if checkbox_product:
                file.IsProduct = True
            checkbox_page = request.POST.getlist('IsPage')
            if checkbox_page:
                file.IsPage = True
            checkbox_category = request.POST.getlist('IsCategory')
            if checkbox_category:
                file.IsCategory = True
            file.IsReview = True
            file.reviewTime = timezone.now()
            file.save()
            messages.success(request, '文件已验收通过！', extra_tags='alert alert-dismissable alert-info')
        else:
            file.delete()
            messages.success(request, '文件已退回，提交人可重新提交！', extra_tags='alert alert-dismissable alert-info')
    else:

        return render(request, 'review_ratefile.html', locals())
    return render(request,'review_ratefile.html',locals())

#复审条款文件
def review_clausefile(request):
    id = request.GET.get('id', None)
    file = ClauseFile.objects.get(pk=id)
    staff = file.staff
    group = staff.group
    directorno = group.directorNo
    assistantno = group.assistantNo
    director = Staff.objects.get(no=directorno)
    assistant = Staff.objects.get(no=assistantno)
    if director == staff:
        check = assistant
    else:
        check = director
    product = file.product
    pro_name = product.name
    name = staff.name
    if request.method == "POST":
        if request.POST.has_key('check'):
            checkbox_company = request.POST.getlist('IsCompany')
            if checkbox_company:
                file.IsCompany = True
            checkbox_product = request.POST.getlist('IsProduct')
            if checkbox_product:
                file.IsProduct = True
            checkbox_page = request.POST.getlist('IsPage')
            if checkbox_page:
                file.IsPage = True
            checkbox_category = request.POST.getlist('IsCategory')
            if checkbox_category:
                file.IsCategory = True
            file.IsReview = True
            file.reviewTime = timezone.now()
            file.save()
            messages.success(request, '文件已验收通过！', extra_tags='alert alert-dismissable alert-info')
        else:
            file.delete()
            messages.success(request, '文件已退回，提交人可重新提交！', extra_tags='alert alert-dismissable alert-info')
    else:

        return render(request, 'review_clausefile.html', locals())
    return render(request,'review_clausefile.html',locals())

#复审现金价值表
def review_cashfile(request):
    id = request.GET.get('id', None)
    file = CashFile.objects.get(pk=id)
    staff = file.staff
    group = staff.group
    directorno = group.directorNo
    assistantno = group.assistantNo
    director = Staff.objects.get(no=directorno)
    assistant = Staff.objects.get(no=assistantno)
    if director == staff:
        check = assistant
    else:
        check = director
    product = file.product
    pro_name = product.name
    name = staff.name
    if request.method == "POST":
        if request.POST.has_key('check'):
            checkbox_company = request.POST.getlist('IsCompany')
            if checkbox_company:
                file.IsCompany = True
            checkbox_product = request.POST.getlist('IsProduct')
            if checkbox_product:
                file.IsProduct = True
            checkbox_page = request.POST.getlist('IsPage')
            if checkbox_page:
                file.IsPage = True
            checkbox_category = request.POST.getlist('IsCategory')
            if checkbox_category:
                file.IsCategory = True
            file.IsReview = True
            file.reviewTime = timezone.now()
            file.save()
            messages.success(request, '文件已验收通过！', extra_tags='alert alert-dismissable alert-info')
        else:
            file.delete()
            messages.success(request, '文件已退回，提交人可重新提交！', extra_tags='alert alert-dismissable alert-info')
    else:
        return render(request, 'review_cashfile.html', locals())
    return render(request,'review_cashfile.html',locals())

#下载费率文件
def load_ratefile(request):
    loginid = request.session['username']
    manager = Manager.objects.get(no=loginid)
    list = RateFile.objects.filter(IsCheck=True)
    list = getPage(request, list)
    if request.method == "POST":
        if request.POST.has_key('filter'):
            c = request.POST['radio']
            if c == 'rate':
                return redirect('/load_ratefile')
            elif c == 'clause':
                return redirect('/load_clausefile')
            else:
                return redirect('/load_cashfile')
        else:
            return render(request, 'load_ratefile.html', locals())
    return render(request,'load_ratefile.html',locals())

#下载条款文件
def load_clausefile(request):
    loginid = request.session['username']
    manager = Manager.objects.get(no=loginid)
    list = ClauseFile.objects.filter(IsCheck=True)
    list = getPage(request, list)
    if request.method == "POST":
        if request.POST.has_key('filter'):
            c = request.POST['radio']
            if c == 'rate':
                return redirect('/load_ratefile')
            elif c == 'clause':
                return redirect('/load_clausefile')
            else:
                return redirect('/load_cashfile')
        else:
            return render(request, 'load_clausefile.html', locals())
    return render(request, 'load_clausefile.html', locals())

#下载现金价值表
def load_cashfile(request):
    loginid = request.session['username']
    manager = Manager.objects.get(no=loginid)
    list = CashFile.objects.filter(IsCheck=True)
    list = getPage(request, list)
    if request.method == "POST":
        if request.POST.has_key('filter'):
            c = request.POST['radio']
            if c == 'rate':
                return redirect('/load_ratefile')
            elif c == 'clause':
                return redirect('/load_clausefile')
            else:
                return redirect('/load_cashfile')
        else:
            return render(request, 'load_cashfile.html', locals())
    return render(request, 'load_cashfile.html', locals())

#获取助理组织概况
def assistantTeam(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    group=staff.group
    project=staff.project
    staff_list=Staff.objects.filter(group=group)
    director=staff_list.get(IsDirector=True)
    manager=project.manager
    return render(request,'assistantTeam.html',locals())

#初审经理个人任务
def check_m_stafftask(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    group = staff.group  # 获取组号
    director=Staff.objects.get(no=group.directorNo)
    list = Task.objects.filter(staff=director).filter(IsGroupTask=False)  # 查出本小组且为经理直接分配到个人的任务
    list = getPage(request, list)
    if request.method == "POST":
        c = request.POST['radio']
        if c == 'task':
            return redirect('/check_m_stafftask')
        else:
            return redirect('/check_m_grouptask')
    return render(request, 'check_m_staffTasK.html', locals())

#初审个人任务产品
def check_m_stafftask_product(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    list = Product.objects.filter(task=task)
    list = getPage(request, list)
    return render(request,'check_m_stafftask_product.html',locals())
#初审经理团队任务
def check_m_grouptask(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    group = staff.group  # 获取组号
    director = Staff.objects.get(no=group.directorNo)
    list = SubTask.objects.filter(staff=director)
    list = getPage(request, list)
    if request.method == "POST":
        c = request.POST['radio']
        if c == 'task':
            return redirect('/check_m_stafftask')
        else:
            return redirect('/check_m_grouptask')
    return render(request, 'check_m_grouptask.html', locals())

#初审经理小组任务产品列表
def check_m_grouptask_product(request):
    id = request.GET.get('id', None)
    task = SubTask.objects.get(pk=id)
    list = Product.objects.filter(subTask=task)
    list = getPage(request, list)
    return render(request,'check_m_grouptask_product.html',locals())

#初审经理任务的产品文件情况
def check_m_product_file(request):
    id = request.GET.get('id', None)
    product = Product.objects.get(pk=id)
    task = product.task
    rateFile_len = len(RateFile.objects.filter(product=product))
    if rateFile_len > 0:
        rateFile = RateFile.objects.get(product=product)
    else:
        rateFile = 0
    clauseFile_len = len(ClauseFile.objects.filter(product=product))
    if clauseFile_len > 0:
        clauseFile = ClauseFile.objects.get(product=product)
    else:
        clauseFile = 0
    cashFile_len = len(CashFile.objects.filter(product=product))
    if cashFile_len > 0:
        cashFile = CashFile.objects.get(product=product)
    else:
        cashFile = 0
    return render(request,'check_m_product_file.html',locals())

#助理个人任务（经理分配）
def a_stafftask_staff(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    list = Task.objects.filter(staff=staff)
    list = getPage(request,list)
    if request.method == "POST":
        c = request.POST['radio']
        if c == 'task':
            return redirect('/a_stafftask_staff')
        else:
            return redirect('/a_stafftask_group')
    return render(request,'a_stafftask_staff.html',locals())

#助理小组任务（主管分配）
def a_stafftask_group(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    list = SubTask.objects.filter(staff=staff)
    list = getPage(request, list)
    if request.method == "POST":
        c = request.POST['radio']
        if c == 'task':
            return redirect('/a_stafftask_staff')
        else:
            return redirect('/a_stafftask_group')

    return render(request,'a_stafftask_group.html',locals())

#助理界面个人任务，小组任务的产品列表
def a_stafftask_group_product(request):
    id = request.GET.get('id', None)
    task = SubTask.objects.get(pk=id)
    list = Product.objects.filter(subTask=task)
    list = getPage(request, list)
    return render(request,'a_stafftask_group_product.html',locals())

#助理界面个人任务，个人任务的产品列表
def a_stafftask_staff_product(request):
    id = request.GET.get('id', None)
    task = Task.objects.get(pk=id)
    list = Product.objects.filter(task=task)
    list = getPage(request, list)
    return render(request,'a_stafftask_staff_product.html',locals())

#助理提交费率文件
def a_submit_ratefile(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    file_list = RateFile.objects.filter(staff=staff)
    file_list = getPage(request, file_list)
    if request.method == "POST":
        if request.POST.has_key('filter'):
            c = request.POST['radio']
            if c == 'rate':
                return redirect('/a_submit_ratefile')
            elif c == 'clause':
                return redirect('/a_submit_clausefile')
            else:
                return redirect('a_submit_cashfile')
        else:
            checkbox_list = request.POST.getlist('checkbox_list')
            if checkbox_list:
                for check in checkbox_list:
                    file = RateFile.objects.get(id=check)
                    file.IsSubmit = True
                    submitTime = timezone.now()
                    file.save()
                    messages.success(request, '提交成功！', extra_tags='alert alert-dismissable alert-info')
                return render(request, 'a_submit_ratefile.html', locals())
            else:
                messages.error(request, '未选中任何文件，请选择！', extra_tags='alert alert-dismissable alert-danger')
                return render(request, 'a_submit_ratefile.html', locals())
    return render(request,'a_submit_ratefile.html',locals())

#助理提交条款文件
def a_submit_clausefile(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    file_list = ClauseFile.objects.filter(staff=staff)
    file_list = getPage(request, file_list)
    if request.method == "POST":
        if request.POST.has_key('filter'):
            c = request.POST['radio']
            if c == 'rate':
                return redirect('/a_submit_ratefile')
            elif c == 'clause':
                return redirect('/a_submit_clausefile')
            else:
                return redirect('a_submit_cashfile')
        else:
            checkbox_list = request.POST.getlist('checkbox_list')
            if checkbox_list:
                for check in checkbox_list:
                    file = ClauseFile.objects.get(id=check)
                    file.IsSubmit = True
                    submitTime = timezone.now()
                    file.save()
                    messages.success(request, '提交成功！', extra_tags='alert alert-dismissable alert-info')
                return render(request, 'a_submit_clausefile.html', locals())
            else:
                messages.error(request, '未选中任何文件，请选择！', extra_tags='alert alert-dismissable alert-danger')
                return render(request, 'a_submit_clausefile.html', locals())
    return render(request, 'a_submit_clausefile.html', locals())

#助理提交现价价值表
def a_submit_cashfile(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    file_list = CashFile.objects.filter(staff=staff)
    file_list = getPage(request, file_list)
    if request.method == "POST":
        if request.POST.has_key('filter'):
            c = request.POST['radio']
            if c == 'rate':
                return redirect('/a_submit_ratefile')
            elif c == 'clause':
                return redirect('/a_submit_clausefile')
            else:
                return redirect('a_submit_cashfile')
        else:
            checkbox_list = request.POST.getlist('checkbox_list')
            if checkbox_list:
                for check in checkbox_list:
                    file = CashFile.objects.get(id=check)
                    file.IsSubmit = True
                    submitTime = timezone.now()
                    file.save()
                    messages.success(request, '提交成功！', extra_tags='alert alert-dismissable alert-info')
                return render(request, 'a_submit_cashfile.html', locals())
            else:
                messages.error(request, '未选中任何文件，请选择！', extra_tags='alert alert-dismissable alert-danger')
                return render(request, 'a_submit_cashfile.html', locals())
    return render(request, 'a_submit_cashfile.html', locals())

#助理产品文件页面
def a_stafftask_staff_productfile(request):
    id = request.GET.get('id', None)
    product = Product.objects.get(pk=id)
    task = product.task
    rateFile_len = len(RateFile.objects.filter(product=product))
    if rateFile_len > 0:
        rateFile = RateFile.objects.get(product=product)
    else:
        rateFile = 0
    clauseFile_len = len(ClauseFile.objects.filter(product=product))
    if clauseFile_len > 0:
        clauseFile = ClauseFile.objects.get(product=product)
    else:
        clauseFile = 0
    cashFile_len = len(CashFile.objects.filter(product=product))
    if cashFile_len > 0:
        cashFile = CashFile.objects.get(product=product)
    else:
        cashFile = 0
    return render(request,'a_stafftask_staff_productfile.html',locals())

#成员组织概况
def staffTeam(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    group = staff.group
    project = staff.project
    list = Staff.objects.filter(group=group)
    director = list.get(IsDirector=True)
    manager = project.manager
    return render(request, 'staffTeam.html', locals())

#成员个人任务列表
def s_stafftask_staff(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    list = Task.objects.filter(staff=staff)
    list = getPage(request, list)
    if request.method == "POST":
        c = request.POST['radio']
        if c == 'task':
            return redirect('/s_stafftask_staff')
        else:
            return redirect('/s_stafftask_group')
    return render(request, 's_stafftask_staff.html', locals())

#成员小组任务列表
def s_stafftask_group(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    list = SubTask.objects.filter(staff=staff)
    list = getPage(request, list)
    if request.method == "POST":
        c = request.POST['radio']
        if c == 'task':
            return redirect('/s_stafftask_staff')
        else:
            return redirect('/s_stafftask_group')
    return render(request, 's_stafftask_group.html', locals())

#成员提交费率文件
def s_submit_ratefile(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    list = RateFile.objects.filter(staff=staff)
    list = getPage(request,list)
    if request.method == "POST":
        if request.POST.has_key('filter'):
            c = request.POST['radio']
            if c == 'rate':
                return redirect('/s_submit_ratefile')
            elif c == 'clause':
                return redirect('/s_submit_clausefile')
            else:
                return redirect('/s_submit_cashfile')
        else:
            checkbox_list = request.POST.getlist('checkbox_list')
            if checkbox_list:
                for check in checkbox_list:
                    file = RateFile.objects.get(id=check)
                    file.IsSubmit = True
                    submitTime = timezone.now()
                    file.save()
                    messages.success(request, '提交成功！', extra_tags='alert alert-dismissable alert-info')
                return render(request, 's_submit_ratefile.html', locals())
            else:
                messages.error(request, '未选中任何文件，请选择！', extra_tags='alert alert-dismissable alert-danger')
                return render(request, 's_submit_ratefile.html', locals())
    return render(request, 's_submit_ratefile.html', locals())

#成员提交条款文件
def s_submit_clausefile(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    list = ClauseFile.objects.filter(staff=staff)
    list = getPage(request, list)
    if request.method == "POST":
        if request.POST.has_key('filter'):
            c = request.POST['radio']
            if c == 'rate':
                return redirect('/s_submit_ratefile')
            elif c == 'clause':
                return redirect('/s_submit_clausefile')
            else:
                return redirect('s_submit_cashfile')
        else:
            checkbox_list = request.POST.getlist('checkbox_list')
            if checkbox_list:
                for check in checkbox_list:
                    file = ClauseFile.objects.get(id=check)
                    file.IsSubmit = True
                    submitTime = timezone.now()
                    file.save()
                    messages.success(request, '提交成功！', extra_tags='alert alert-dismissable alert-info')
                return render(request, 's_submit_clausefile.html', locals())
            else:
                messages.error(request, '未选中任何文件，请选择！', extra_tags='alert alert-dismissable alert-danger')
                return render(request, 's_submit_clausefile.html', locals())
    return render(request, 's_submit_clausefile.html', locals())

#成员提交现金价值表
def s_submit_cashfile(request):
    loginid = request.session['username']
    staff = Staff.objects.get(no=loginid)
    list = CashFile.objects.filter(staff=staff)
    list = getPage(request, list)
    if request.method == "POST":
        if request.POST.has_key('filter'):
            c = request.POST['radio']
            if c == 'rate':
                return redirect('/s_submit_ratefile')
            elif c == 'clause':
                return redirect('/s_submit_clausefile')
            else:
                return redirect('s_submit_cashfile')
        else:
            checkbox_list = request.POST.getlist('checkbox_list')
            if checkbox_list:
                for check in checkbox_list:
                    file = CashFile.objects.get(id=check)
                    file.IsSubmit = True
                    submitTime = timezone.now()
                    file.save()
                    messages.success(request, '提交成功！', extra_tags='alert alert-dismissable alert-info')
                return render(request, 's_submit_cashfile.html', locals())
            else:
                messages.error(request, '未选中任何文件，请选择！', extra_tags='alert alert-dismissable alert-danger')
                return render(request, 's_submit_cashfile.html', locals())
    return render(request, 's_submit_cashfile.html', locals())