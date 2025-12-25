from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, DeleteView
from django.views.decorators.http import require_http_methods
from .models import Bb, Rubric
from .forms import BbForm


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbRubricBbsView(ListView):
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = get_object_or_404(Rubric, pk=self.kwargs['rubric_id'])
        return context


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context



def add(request):
    bbf = BbForm()
    context = {'form': bbf}
    return render(request, 'add.html', context)


@require_http_methods(['GET', 'POST'])
def add_and_save(request):
    rubrics = get_list_or_404(Rubric)

    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(
                reverse('bboard:by_rubric',
                        kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf, 'rubrics': rubrics}
            return render(request, 'add.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf, 'rubrics': rubrics}
        return render(request, 'add.html', context)


def bb_detail(request, bb_id):
    bb = get_object_or_404(Bb, pk=bb_id)
    context = {'bb': bb}
    return render(request, 'bb_detail.html', context)



def update_titles_view(request):
    """Обновляем все заголовки Bb: title + (id)"""
    Bb.update_titles()
    return HttpResponseRedirect(reverse('bboard:index'))  # Перенаправление на главную

def delete_odd_titles_view(request):
    """Удаляем объявления с нечётной цифрой в заголовке"""
    Bb.delete_odd_titles()
    return HttpResponseRedirect(reverse('bboard:index'))
