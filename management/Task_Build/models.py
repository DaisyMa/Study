#coding:utf-8
from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Manager(models.Model):
    no = models.CharField(max_length=50,verbose_name="经理编号")
    name=models.CharField(max_length=30,verbose_name="姓名")
    email = models.EmailField(verbose_name="邮箱 ")
    phone = models.BigIntegerField(verbose_name="手机号码")
    pwd=models.CharField(max_length=30,null=True)

    def __unicode__(self):
        return str(self.no)

class Project(models.Model):
    no = models.CharField(max_length=50,verbose_name="项目编号")
    name=models.CharField(max_length=50,verbose_name="项目名称")
    releaseTime=models.DateField(auto_now_add=True,verbose_name="发布时间")
    deadline=models.DateField(verbose_name="截止时间")
    staffNum = models.IntegerField(verbose_name="人员数量",default=0)
    productNum=models.IntegerField(verbose_name="产品数量")
    content=models.TextField(max_length=100,verbose_name="项目描述")
    manager=models.ForeignKey(Manager,verbose_name="项目经理")

    def __unicode__(self):
        return str(self.no)


class Group(models.Model):
    no = models.CharField(max_length=50,verbose_name="小组编号")
    name=models.CharField(max_length=50,verbose_name="小组名称")
    staffNum=models.IntegerField(verbose_name="小组人数")
    project=models.ForeignKey(Project,verbose_name="项目编号")
    directorNo=models.CharField(max_length=50,verbose_name="主管编号",null=True)
    assistantNo = models.CharField(max_length=50, verbose_name="助理编号",null=True)

    def __unicode__(self):
        return str(self.no)


class Staff(models.Model):
    no = models.CharField(max_length=50,verbose_name="员工编号")
    name=models.CharField(max_length=30,verbose_name="姓名")
    sex = models.CharField(max_length=10,verbose_name="性别")
    grade=models.CharField(max_length=30,verbose_name="年级")
    phone=models.BigIntegerField(verbose_name="手机号码")
    email = models.EmailField(verbose_name="邮箱地址")
    IsDirector=models.BooleanField(verbose_name="是否负责人",default=0)
    IsAssistant=models.BooleanField(verbose_name="是否助理",default=0)
    project=models.ForeignKey(Project,verbose_name="项目编号",null=True)
    group=models.ForeignKey(Group,verbose_name="小组编号",null=True)

    def __unicode__(self):
        return str(self.no)

class Task(models.Model):
    no = models.CharField(max_length=50, verbose_name="任务编号")
    productNum = models.IntegerField(verbose_name="产品数量")
    addTime = models.DateField(auto_now_add=True, verbose_name="创建时间")
    deadline = models.DateField(verbose_name="截止时间", null=True)
    group = models.ForeignKey(Group, verbose_name="小组编号", null=True)
    staff = models.ForeignKey(Staff, verbose_name="成员编号", null=True)
    note = models.CharField(max_length=50, verbose_name="任务公告")
    project = models.ForeignKey(Project, verbose_name="项目编号",null=True)
    IsReallot=models.BooleanField(verbose_name="是否再分配",default=0)
    IsAllot=models.BooleanField(verbose_name="是否分配",default=0)
    allotTime=models.DateField(verbose_name="分配时间",null=True)
    IsGroupTask=models.BooleanField(verbose_name="是否小组任务",default=0)

class SubTask(models.Model):
    no = models.CharField(max_length=50, verbose_name="子任务编号")
    productNum = models.IntegerField(verbose_name="产品数量")
    addTime = models.DateField(auto_now_add=True, verbose_name="创建时间")
    deadline = models.DateField(verbose_name="截止时间", null=True)
    staff = models.ForeignKey(Staff, verbose_name="成员编号", null=True)
    note = models.CharField(max_length=50, verbose_name="任务公告")
    task = models.ForeignKey(Task, verbose_name="任务编号",null=True)
    IsAllot=models.BooleanField(verbose_name="是否分配",default=0)
    allotTime = models.DateField(verbose_name="分配时间",null=True)


class Product(models.Model):
    no = models.CharField(max_length=50,verbose_name="产品编号")
    name=models.CharField(max_length=50,verbose_name="产品名称")
    category=models.CharField(max_length=30,verbose_name="产品分类")
    company=models.CharField(max_length=30,verbose_name="所属公司")
    importTime=models.DateField(auto_now_add=True,verbose_name="导入时间",null=True)
    project=models.ForeignKey(Project,verbose_name="项目编号")
    task=models.ForeignKey(Task,verbose_name="任务编号",null=True)
    subTask=models.ForeignKey(SubTask,verbose_name="任务编号",null=True)

    def __unicode__(self):
       return str(self.no)

#解析文件
class ImportFile(models.Model):
    file = models.FileField(upload_to='./upload/')

    def __str__(self):
        return self.file

#费率文件
class RateFile(models.Model):
    no = models.CharField(max_length=50, verbose_name="文件编号", default='')
    file = models.FileField(upload_to='./upload')
    name = models.CharField(max_length=50, verbose_name="文件名称")
    pageNum = models.IntegerField(verbose_name="总页数")
    product = models.ForeignKey(Product, verbose_name="产品编号")
    staff = models.ForeignKey(Staff, verbose_name="提交人")
    IsSubmit = models.BooleanField(verbose_name="是否提交", default=0)
    submitTime = models.DateField(verbose_name="提交时间", null=True)
    IsCheck = models.BooleanField(verbose_name="是否初审通过", default=0)
    checkTime = models.DateField(verbose_name="复审时间", null=True)
    IsReview = models.BooleanField(verbose_name="提交时间", default=0)
    reviewTime = models.DateField(verbose_name="验收时间", null=True)
    IsReturn = models.BooleanField(verbose_name="是否退回", default=0)
    fileNote = models.CharField(verbose_name="文件说明", max_length=50, null=True)
    uploadTime = models.DateField(auto_now_add=True,verbose_name="上传时间", null=True)
    returnTime = models.IntegerField(verbose_name="文件退回次数",default=0)
    returnDate = models.DateField(verbose_name="文件退回日期", null=True)
    IsCompany = models.BooleanField(verbose_name="公司名称一致", default=0)
    IsPage = models.BooleanField(verbose_name="文件页数一致", default=0)
    IsCategory = models.BooleanField(verbose_name="文件类型一致", default=0)
    IsCheckOk = models.BooleanField(verbose_name="初审结果正确", default=0)
    IsProduct = models.BooleanField(verbose_name="产品名称一致", default=0)
    IsCheckPass=models.BooleanField(verbose_name="初审是否通过", default=0)

#条款文件
class ClauseFile(models.Model):
    no = models.CharField(max_length=50, verbose_name="文件编号", default='')
    file = models.FileField(upload_to='./upload')
    name = models.CharField(max_length=50, verbose_name="文件名称")
    pageNum = models.IntegerField(verbose_name="总页数")
    product = models.ForeignKey(Product, verbose_name="产品编号")
    staff = models.ForeignKey(Staff, verbose_name="提交人")
    IsSubmit = models.BooleanField(verbose_name="是否提交", default=0)
    submitTime = models.DateField(verbose_name="提交时间", null=True)
    IsCheck = models.BooleanField(verbose_name="是否验收", default=0)
    checkTime = models.DateField(verbose_name="复审时间", null=True)
    IsReview = models.BooleanField(verbose_name="提交时间", default=0)
    reviewTime = models.DateField(verbose_name="验收时间", null=True)
    IsReturn = models.BooleanField(verbose_name="是否退回", default=0)
    fileNote = models.CharField(verbose_name="文件说明", max_length=50, null=True)
    uploadTime = models.DateField(auto_now_add=True,verbose_name="上传时间", null=True)
    returnTime = models.IntegerField(verbose_name="文件退回次数",default=0)
    returnDate = models.DateField(verbose_name="文件退回日期", null=True)
    IsCompany = models.BooleanField(verbose_name="公司名称一致", default=0)
    IsPage = models.BooleanField(verbose_name="文件页数一致", default=0)
    IsCategory = models.BooleanField(verbose_name="文件类型一致", default=0)
    IsCheckOk = models.BooleanField(verbose_name="初审结果正确", default=0)
    IsProduct = models.BooleanField(verbose_name="产品名称一致", default=0)
    IsCheckPass=models.BooleanField(verbose_name="初审是否通过", default=0)

#现金表文件
class CashFile(models.Model):
    no = models.CharField(max_length=50, verbose_name="文件编号",default='')
    file = models.FileField(upload_to='./upload')
    name = models.CharField(max_length=50, verbose_name="文件名称")
    pageNum = models.IntegerField(verbose_name="总页数")
    product = models.ForeignKey(Product, verbose_name="产品编号")
    staff = models.ForeignKey(Staff, verbose_name="提交人")
    IsSubmit = models.BooleanField(verbose_name="是否提交", default=0)
    submitTime=models.DateField(verbose_name="提交时间", null=True)
    IsCheck = models.BooleanField(verbose_name="是否验收", default=0)
    checkTime=models.DateField(verbose_name="复审时间",null=True)
    IsReview = models.BooleanField(verbose_name="提交时间", default=0)
    reviewTime = models.DateField(verbose_name="验收时间",null=True)
    IsReturn = models.BooleanField(verbose_name="是否退回", default=0)
    fileNote = models.CharField(verbose_name="文件说明", max_length=50,null=True)
    uploadTime=models.DateField(auto_now_add=True,verbose_name="上传时间",null=True)
    returnTime=models.IntegerField(verbose_name="文件退回次数",default=0)
    returnDate= models.DateField(verbose_name="文件退回日期",default=0)
    IsCompany= models.BooleanField(verbose_name="公司名称一致", default=0)
    IsPage= models.BooleanField(verbose_name="文件页数一致", default=0)
    IsCategory= models.BooleanField(verbose_name="文件类型一致", default=0)
    IsCheckOk= models.BooleanField(verbose_name="初审结果正确", default=0)
    IsProduct= models.BooleanField(verbose_name="产品名称一致", default=0)
    IsCheckPass = models.BooleanField(verbose_name="初审是否通过", default=0)
