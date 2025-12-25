from bboard.views import update_titles_view, delete_odd_titles_view

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', BbRubricBbsView.as_view(), name='by_rubric'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', BbEditView.as_view(), name='edit'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),


    path('update_titles/', update_titles_view, name='update_titles'),
    path('delete_odd/', delete_odd_titles_view, name='delete_odd_titles'),

    path('', index, name='index'),
]
