#coding=UTF-8
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Choice, Question
# Create your views here.
#http://python.usyiyi.cn/django/intro/tutorial03.html

#通用视图
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#视图渲染程序 优化前
# def index(request):
# 	#return HttpResponse("Hello,world.You're at the polls index.")
#     #获取列表
#     latest_question_list=Question.objects.order_by('-pub_date')[:5]
#     #函数渲染
#     #output=','.join([p.question_text for p in latest_question_list])
#     #调用模版渲染  填充一个context Context是一个字典，将模板变量的名字映射到Python 对象
#     #template=loader.get_template('polls/index.html')
#     '''context =RequestContext(request,{
#         'latest_question_list':latest_question_list,
#         })
#     return HttpResponse(template.render(context))
#     '''
#     #render 快捷方式
#     context = {'latest_question_list':latest_question_list}
#     return render(request,'polls/index.html',context)

# def results(request,question_id):
#     #response="You're looking at the results of quesiton %s"  
#     #return HttpResponse(response % question_id)
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/results.html',{'question':question})
# def detail(request,question_id):
#     #try:
#     #    question =Question.objects.get(pk=question_id)
#     #except Question.DoesNotExist:
#     #    
#     #    raise Http404("Question does not exist")
#     #快捷方式get_object_or_404()
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,'polls/detail.html',{'question':question})
#     #return HttpResponse("You're looking at the results of quesiton %s" % question_id)
def vote(request,question_id):
    #return HttpResponse("You're voting on quesiton %s" % question_id)
    p=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice= p.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        #Redisplay the question voting form.
        return render(request, 'polls/detail.html',{
            'question': p,
            'error_message':"You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))