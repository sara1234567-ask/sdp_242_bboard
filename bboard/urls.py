from django.urls import path
from django.views.generic import CreateView

from bboard.models import Bb
from bboard.views import (index, by_rubric, BbCreateView,
                          add, add_and_save,
                          BbRubricBbsView, BbDetailView, BbEditView, BbDeleteView)

app_name = 'bboard'

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    # path('add/', CreateView.as_view(model=Bb,
    #                                   template_name='create.html')),
    # path('add/', add_and_save, name='add'),

    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('<int:rubric_id>/', BbRubricBbsView.as_view(), name='by_rubric'),

    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),

    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),

    path('', index, name='index'),
]