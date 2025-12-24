from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.http import require_GET, require_POST, require_safe, require_http_methods
from django.views.generic import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView

from bboard.forms import BbForm
from bboard.models import Bb, Rubric


def index(request):
    rubrics = Rubric.objects.all()
    bbs = Bb.objects.all()

    paginator = Paginator(bbs, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    context = {'bbs': page.object_list, 'page': page, 'rubrics': rubrics}

    return render(request, 'index.html', context)


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'by_rubric.html', context)


class BbCreateView(CreateView):
    template_name = 'bboard/bb_create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def get_success_url(self):
        return reverse('bboard:by_rubric',
                       kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('bboard:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/{rubric_id}'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


class BbRubricBbsView(ListView):
    # template_name = 'by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context


class BbDetailView(DetailView):
    model = Bb
    # template_name = 'bb_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


def add(request):
    bbf = BbForm()
    context = {'form': bbf}
    return render(request, 'add.html', context)


# @require_GET
# @require_POST
# @require_safe
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
