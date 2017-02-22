from django.http import HttpResponseRedirect
# from django.http import Http404, HttpResponse
# from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question, Choice

# wersja z HttpResponse i loader
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#
#     # uniezależniamy się od kodu pythona
#     # listowanie pytań robimy w szablonie
#     # output = ', '.join([q.question_text for q in latest_question_list])
#
#     return HttpResponse(template.render(context, request))


# wersja z render
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    # na skróty z get_object_or_404()
    # dla filter() mamy funkcję get_list_or_404()
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # ponowne wyświetlenie formularza
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # po sukcesie POST używamy HttpResponseRedirect (web dev)
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
