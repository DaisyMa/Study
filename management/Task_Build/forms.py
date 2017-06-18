# coding:utf-8
from django import forms
from Task_Build.models import *
from django.utils import timezone
from django.contrib.admin import widgets

class LoginForm(forms.Form):

    username = forms.CharField(label='账号', widget=forms.TextInput(attrs={"placeholder": "工号", "required": "required",}),
                               max_length=50, error_messages={"required": "账号不能为空", })
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={"placeholder": "邮箱", "required": "required", }) ,
    error_messages={"required": "密码不能为空",})

class AddProjectForm(forms.Form):
    name = forms.CharField(label="项目名称",widget=forms.TextInput(attrs={'class':'form-control'}))

    #deadline=forms.DateInput()
    staffNum = forms.IntegerField(label="人员数量",widget=forms.NumberInput(attrs={'class':'form-control'}))
    productNum = forms.IntegerField(label="产品数量",widget=forms.NumberInput(attrs={'class':'form-control'}))
    content = forms.CharField(label='项目描述',widget=forms.Textarea(attrs={'class':"form-control"}))

class EditProject(forms.ModelForm):
    class Meta:
        model=Project
        name = forms.CharField(widget=forms.TextInput(attrs={'class': 'special'}))
        content = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))
        exclude=['id','manager']


def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args,**kwargs)
        self.fields['no'].widget.attrs['readonly'] = True
        self.fields['releaseTime'].widget.attrs['readonly'] = True

class ChangepwdForm(forms.Form):
    oldpwd= forms.CharField(label='原密码',widget=forms.TextInput(attrs={"placeholder": "工号", "required": "required",}),
                            max_length=50, error_messages={"required": "请输入原密码", })
    newpwd1 = forms.CharField(
        label="新密码",
        error_messages={'required': '请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':"新密码",
                "required": "required",
            }
        ),
    )
    newpwd2 = forms.CharField(
        label="确认密码",
        error_messages={'required': '请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':"确认密码",
                "required": "required",
            }
        ),
    )

class UploadFileForm(forms.Form):
    file = forms.FileField(label="请选择文件")

class AddGroup(forms.Form):
    groupname = forms.CharField(label="小组名称",widget=forms.TextInput(attrs={'class':'form-control'}))
    staffnum = forms.IntegerField(label="小组人数",widget=forms.NumberInput(attrs={'class':'form-control'}))

class UploadFileInfo(forms.Form):
   # RADIO_CHOICES = (
      #  ('rate', "费率文件"),
        #('clause', "条款文件 "),
      #  ('cash', "现金价值表 "),
    #)
   # fileCategory=forms.ChoiceField(label="请选择文件类型",widget = forms.RadioSelect, choices = RADIO_CHOICES)
    pageNum = forms.IntegerField(label="文件页数", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    filenote= forms.CharField(label="文件说明", widget=forms.TextInput(attrs={'class': 'form-control'}))
    file = forms.FileField(label="请选择文件")
