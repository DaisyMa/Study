# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-10 09:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(default='', max_length=50, verbose_name='\u6587\u4ef6\u7f16\u53f7')),
                ('file', models.FileField(upload_to='./upload')),
                ('name', models.CharField(max_length=50, verbose_name='\u6587\u4ef6\u540d\u79f0')),
                ('pageNum', models.IntegerField(verbose_name='\u603b\u9875\u6570')),
                ('IsSubmit', models.BooleanField(default=0, verbose_name='\u662f\u5426\u63d0\u4ea4')),
                ('submitTime', models.DateField(null=True, verbose_name='\u63d0\u4ea4\u65f6\u95f4')),
                ('IsCheck', models.BooleanField(default=0, verbose_name='\u662f\u5426\u9a8c\u6536')),
                ('checkTime', models.DateField(null=True, verbose_name='\u590d\u5ba1\u65f6\u95f4')),
                ('IsReview', models.BooleanField(default=0, verbose_name='\u63d0\u4ea4\u65f6\u95f4')),
                ('reviewTime', models.DateField(null=True, verbose_name='\u9a8c\u6536\u65f6\u95f4')),
                ('IsReturn', models.BooleanField(default=0, verbose_name='\u662f\u5426\u9000\u56de')),
                ('fileNote', models.CharField(max_length=50, null=True, verbose_name='\u6587\u4ef6\u8bf4\u660e')),
                ('uploadTime', models.DateField(null=True, verbose_name='\u4e0a\u4f20\u65f6\u95f4')),
                ('returnTime', models.IntegerField(default=0, verbose_name='\u6587\u4ef6\u9000\u56de\u6b21\u6570')),
                ('returnDate', models.DateField(default=0, verbose_name='\u6587\u4ef6\u9000\u56de\u65e5\u671f')),
                ('IsCompany', models.BooleanField(default=0, verbose_name='\u516c\u53f8\u540d\u79f0\u4e00\u81f4')),
                ('IsPage', models.BooleanField(default=0, verbose_name='\u6587\u4ef6\u9875\u6570\u4e00\u81f4')),
                ('IsCategory', models.BooleanField(default=0, verbose_name='\u6587\u4ef6\u7c7b\u578b\u4e00\u81f4')),
                ('IsCheckOk', models.BooleanField(default=0, verbose_name='\u521d\u5ba1\u7ed3\u679c\u6b63\u786e')),
                ('IsProduct', models.BooleanField(default=0, verbose_name='\u4ea7\u54c1\u540d\u79f0\u4e00\u81f4')),
            ],
        ),
        migrations.CreateModel(
            name='ClauseFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(default='', max_length=50, verbose_name='\u6587\u4ef6\u7f16\u53f7')),
                ('file', models.FileField(upload_to='./upload')),
                ('name', models.CharField(max_length=50, verbose_name='\u6587\u4ef6\u540d\u79f0')),
                ('pageNum', models.IntegerField(verbose_name='\u603b\u9875\u6570')),
                ('IsSubmit', models.BooleanField(default=0, verbose_name='\u662f\u5426\u63d0\u4ea4')),
                ('submitTime', models.DateField(null=True, verbose_name='\u63d0\u4ea4\u65f6\u95f4')),
                ('IsCheck', models.BooleanField(default=0, verbose_name='\u662f\u5426\u9a8c\u6536')),
                ('checkTime', models.DateField(null=True, verbose_name='\u590d\u5ba1\u65f6\u95f4')),
                ('IsReview', models.BooleanField(default=0, verbose_name='\u63d0\u4ea4\u65f6\u95f4')),
                ('reviewTime', models.DateField(null=True, verbose_name='\u9a8c\u6536\u65f6\u95f4')),
                ('IsReturn', models.BooleanField(default=0, verbose_name='\u662f\u5426\u9000\u56de')),
                ('fileNote', models.CharField(max_length=50, null=True, verbose_name='\u6587\u4ef6\u8bf4\u660e')),
                ('uploadTime', models.DateField(null=True, verbose_name='\u4e0a\u4f20\u65f6\u95f4')),
                ('returnTime', models.IntegerField(default=0, verbose_name='\u6587\u4ef6\u9000\u56de\u6b21\u6570')),
                ('returnDate', models.DateField(null=True, verbose_name='\u6587\u4ef6\u9000\u56de\u65e5\u671f')),
                ('IsCompany', models.BooleanField(default=0, verbose_name='\u516c\u53f8\u540d\u79f0\u4e00\u81f4')),
                ('IsPage', models.BooleanField(default=0, verbose_name='\u6587\u4ef6\u9875\u6570\u4e00\u81f4')),
                ('IsCategory', models.BooleanField(default=0, verbose_name='\u6587\u4ef6\u7c7b\u578b\u4e00\u81f4')),
                ('IsCheckOk', models.BooleanField(default=0, verbose_name='\u521d\u5ba1\u7ed3\u679c\u6b63\u786e')),
                ('IsProduct', models.BooleanField(default=0, verbose_name='\u4ea7\u54c1\u540d\u79f0\u4e00\u81f4')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=50, verbose_name='\u5c0f\u7ec4\u7f16\u53f7')),
                ('name', models.CharField(max_length=50, verbose_name='\u5c0f\u7ec4\u540d\u79f0')),
                ('staffNum', models.IntegerField(verbose_name='\u5c0f\u7ec4\u4eba\u6570')),
                ('directorNo', models.CharField(max_length=50, null=True, verbose_name='\u4e3b\u7ba1\u7f16\u53f7')),
                ('assistantNo', models.CharField(max_length=50, null=True, verbose_name='\u52a9\u7406\u7f16\u53f7')),
            ],
        ),
        migrations.CreateModel(
            name='ImportFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='./upload/')),
            ],
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=50, verbose_name='\u7ecf\u7406\u7f16\u53f7')),
                ('name', models.CharField(max_length=30, verbose_name='\u59d3\u540d')),
                ('email', models.EmailField(max_length=254, verbose_name='\u90ae\u7bb1 ')),
                ('phone', models.BigIntegerField(verbose_name='\u624b\u673a\u53f7\u7801')),
                ('pwd', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=50, verbose_name='\u4ea7\u54c1\u7f16\u53f7')),
                ('name', models.CharField(max_length=50, verbose_name='\u4ea7\u54c1\u540d\u79f0')),
                ('category', models.CharField(max_length=30, verbose_name='\u4ea7\u54c1\u5206\u7c7b')),
                ('company', models.CharField(max_length=30, verbose_name='\u6240\u5c5e\u516c\u53f8')),
                ('importTime', models.DateField(auto_now_add=True, null=True, verbose_name='\u5bfc\u5165\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=50, verbose_name='\u9879\u76ee\u7f16\u53f7')),
                ('name', models.CharField(max_length=50, verbose_name='\u9879\u76ee\u540d\u79f0')),
                ('releaseTime', models.DateField(auto_now_add=True, verbose_name='\u53d1\u5e03\u65f6\u95f4')),
                ('deadline', models.DateField(verbose_name='\u622a\u6b62\u65f6\u95f4')),
                ('staffNum', models.IntegerField(default=0, verbose_name='\u4eba\u5458\u6570\u91cf')),
                ('productNum', models.IntegerField(verbose_name='\u4ea7\u54c1\u6570\u91cf')),
                ('content', models.TextField(max_length=100, verbose_name='\u9879\u76ee\u63cf\u8ff0')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Manager', verbose_name='\u9879\u76ee\u7ecf\u7406')),
            ],
        ),
        migrations.CreateModel(
            name='RateFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(default='', max_length=50, verbose_name='\u6587\u4ef6\u7f16\u53f7')),
                ('file', models.FileField(upload_to='./upload')),
                ('name', models.CharField(max_length=50, verbose_name='\u6587\u4ef6\u540d\u79f0')),
                ('pageNum', models.IntegerField(verbose_name='\u603b\u9875\u6570')),
                ('IsSubmit', models.BooleanField(default=0, verbose_name='\u662f\u5426\u63d0\u4ea4')),
                ('submitTime', models.DateField(null=True, verbose_name='\u63d0\u4ea4\u65f6\u95f4')),
                ('IsCheck', models.BooleanField(default=0, verbose_name='\u662f\u5426\u9a8c\u6536')),
                ('checkTime', models.DateField(null=True, verbose_name='\u590d\u5ba1\u65f6\u95f4')),
                ('IsReview', models.BooleanField(default=0, verbose_name='\u63d0\u4ea4\u65f6\u95f4')),
                ('reviewTime', models.DateField(null=True, verbose_name='\u9a8c\u6536\u65f6\u95f4')),
                ('IsReturn', models.BooleanField(default=0, verbose_name='\u662f\u5426\u9000\u56de')),
                ('fileNote', models.CharField(max_length=50, null=True, verbose_name='\u6587\u4ef6\u8bf4\u660e')),
                ('uploadTime', models.DateField(null=True, verbose_name='\u4e0a\u4f20\u65f6\u95f4')),
                ('returnTime', models.IntegerField(default=0, verbose_name='\u6587\u4ef6\u9000\u56de\u6b21\u6570')),
                ('returnDate', models.DateField(null=True, verbose_name='\u6587\u4ef6\u9000\u56de\u65e5\u671f')),
                ('IsCompany', models.BooleanField(default=0, verbose_name='\u516c\u53f8\u540d\u79f0\u4e00\u81f4')),
                ('IsPage', models.BooleanField(default=0, verbose_name='\u6587\u4ef6\u9875\u6570\u4e00\u81f4')),
                ('IsCategory', models.BooleanField(default=0, verbose_name='\u6587\u4ef6\u7c7b\u578b\u4e00\u81f4')),
                ('IsCheckOk', models.BooleanField(default=0, verbose_name='\u521d\u5ba1\u7ed3\u679c\u6b63\u786e')),
                ('IsProduct', models.BooleanField(default=0, verbose_name='\u4ea7\u54c1\u540d\u79f0\u4e00\u81f4')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Product', verbose_name='\u4ea7\u54c1\u7f16\u53f7')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=50, verbose_name='\u5458\u5de5\u7f16\u53f7')),
                ('name', models.CharField(max_length=30, verbose_name='\u59d3\u540d')),
                ('sex', models.CharField(max_length=10, verbose_name='\u6027\u522b')),
                ('grade', models.CharField(max_length=30, verbose_name='\u5e74\u7ea7')),
                ('phone', models.BigIntegerField(verbose_name='\u624b\u673a\u53f7\u7801')),
                ('email', models.EmailField(max_length=254, verbose_name='\u90ae\u7bb1\u5730\u5740')),
                ('IsDirector', models.BooleanField(default=0, verbose_name='\u662f\u5426\u8d1f\u8d23\u4eba')),
                ('IsAssistant', models.BooleanField(default=0, verbose_name='\u662f\u5426\u52a9\u7406')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Group', verbose_name='\u5c0f\u7ec4\u7f16\u53f7')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Project', verbose_name='\u9879\u76ee\u7f16\u53f7')),
            ],
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=50, verbose_name='\u5b50\u4efb\u52a1\u7f16\u53f7')),
                ('productNum', models.IntegerField(verbose_name='\u4ea7\u54c1\u6570\u91cf')),
                ('addTime', models.DateField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('deadline', models.DateField(null=True, verbose_name='\u622a\u6b62\u65f6\u95f4')),
                ('note', models.CharField(max_length=50, verbose_name='\u4efb\u52a1\u516c\u544a')),
                ('IsAllot', models.BooleanField(default=0, verbose_name='\u662f\u5426\u5206\u914d')),
                ('allotTime', models.DateField(null=True, verbose_name='\u5206\u914d\u65f6\u95f4')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Staff', verbose_name='\u6210\u5458\u7f16\u53f7')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=50, verbose_name='\u4efb\u52a1\u7f16\u53f7')),
                ('productNum', models.IntegerField(verbose_name='\u4ea7\u54c1\u6570\u91cf')),
                ('addTime', models.DateField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('deadline', models.DateField(null=True, verbose_name='\u622a\u6b62\u65f6\u95f4')),
                ('note', models.CharField(max_length=50, verbose_name='\u4efb\u52a1\u516c\u544a')),
                ('IsReallot', models.BooleanField(default=0, verbose_name='\u662f\u5426\u518d\u5206\u914d')),
                ('IsAllot', models.BooleanField(default=0, verbose_name='\u662f\u5426\u5206\u914d')),
                ('allotTime', models.DateField(null=True, verbose_name='\u5206\u914d\u65f6\u95f4')),
                ('IsGroupTask', models.BooleanField(default=0, verbose_name='\u662f\u5426\u5c0f\u7ec4\u4efb\u52a1')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Group', verbose_name='\u5c0f\u7ec4\u7f16\u53f7')),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Project', verbose_name='\u9879\u76ee\u7f16\u53f7')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Staff', verbose_name='\u6210\u5458\u7f16\u53f7')),
            ],
        ),
        migrations.AddField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Task', verbose_name='\u4efb\u52a1\u7f16\u53f7'),
        ),
        migrations.AddField(
            model_name='ratefile',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Staff', verbose_name='\u63d0\u4ea4\u4eba'),
        ),
        migrations.AddField(
            model_name='product',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Project', verbose_name='\u9879\u76ee\u7f16\u53f7'),
        ),
        migrations.AddField(
            model_name='product',
            name='subTask',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Task_Build.SubTask', verbose_name='\u4efb\u52a1\u7f16\u53f7'),
        ),
        migrations.AddField(
            model_name='product',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Task', verbose_name='\u4efb\u52a1\u7f16\u53f7'),
        ),
        migrations.AddField(
            model_name='group',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Project', verbose_name='\u9879\u76ee\u7f16\u53f7'),
        ),
        migrations.AddField(
            model_name='clausefile',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Product', verbose_name='\u4ea7\u54c1\u7f16\u53f7'),
        ),
        migrations.AddField(
            model_name='clausefile',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Staff', verbose_name='\u63d0\u4ea4\u4eba'),
        ),
        migrations.AddField(
            model_name='cashfile',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Product', verbose_name='\u4ea7\u54c1\u7f16\u53f7'),
        ),
        migrations.AddField(
            model_name='cashfile',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Task_Build.Staff', verbose_name='\u63d0\u4ea4\u4eba'),
        ),
    ]
