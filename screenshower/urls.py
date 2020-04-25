from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('pricing', views.pricing, name='pricing'),

    # app
    path('app/project/', views.project_list, name='project_list'),
    path('app/project/new/', views.project_new, name='project_new'),
    path('app/project/<int:pk>/', views.project_detail, name='project_detail'),
    path('app/project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('app/project/<int:pk>/app/', views.app, name='app'),
    path('app/project/paroi/<int:pk>', views.paroi_edit, name='paroi_edit'),
    path('app/project/<int:pk>/remove/', views.project_remove, name='project_remove'),

    path('app/models/', views.models_list, name='model_list'),
    path('app/models/new/', views.model_new, name='model_new'),
    path('app/models/<int:pk>/', views.model_detail, name='model_detail'),
    path('app/models/<int:pk>/duplicate/', views.model_duplicate, name='model_duplicate'),


    path('app/piece/new/', views.piece_new, name='piece_new'),
    path('app/piece/<int:pk>/edit/', views.piece_edit, name='piece_edit')

]