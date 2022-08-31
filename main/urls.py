from django.urls import path
from .views import TabelView, CreateOtpuskView
from . import views


urlpatterns = [
    path('', views.index, name = 'index' ),
    path('createcard/', views.createcard, name = 'createcard' ),
    path('search/', views.search, name = 'search' ),
    #path('createotpusk/<int:id_man>/', views.createotpusk, name = 'createotpusk' ),
    path('createotpusk/<int:id_man>/', CreateOtpuskView.as_view(), name = 'createotpusk' ),

    path('createworkday/<int:id_man>/<str:data_work_id>/<str:data_work>/<str:data_day>/<str:data_month>/<str:data_year>/', views.createworkday, name = 'createworkday' ),
    path('preview/<int:id>/', views.preview, name = 'preview' ),
    path('edit/<int:id>/', views.edit, name = 'edit' ),
    path('del/<int:id>/', views.delete, name = 'del' ),
    path('proba', views.proba, name = 'proba' ),

    path('editOtpusk/<int:id_otpusk>/<str:title_otpusk>/', views.editOtpusk, name = 'editOtpusk' ),
    path('delOtpusk/<int:id_otpusk>/', views.del_Otpusk, name = 'delOtpusk' ),
    path('watchfoto/<int:id_otpusk>/<str:id_man>/', views.watchfoto, name = 'watchfoto' ),
    path('tabel/', TabelView.as_view(), name = 'tabel' ),
    path('tabeledit/<int:id>/<str:data_work>/<str:data_day>/<str:data_month>/<str:data_year>/', views.tabeledit, name='tabeledit'),
    #path('probaa/', ProbaView.as_view(), name='probaa'),


]