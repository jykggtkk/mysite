#coding=utf-8
from django.contrib import admin

from .models import Question,Choice


# Register your models here.
#如果后面有类用到这个类  这个类要放在前面
#admin.StackedInline 默认声明
#admin.TabularInline 列表模式
class ChoiceInline(admin.TabularInline):
    model=Choice
    extra=3

class QuestionAdmin(admin.ModelAdmin):
    #fields=['pub_date','question_text']
    fieldsets =[
        (None,            {'fields':['question_text']}),
        ('创建时间',{'fields':['pub_date'],'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display=('question_text','pub_date','was_published_recently')
    list_filter=['pub_date']
    search_fields=['question_text']


admin.site.register(Question,QuestionAdmin)

#admin.site.register(Choice)
