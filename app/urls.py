from django.urls import path

from app import views

urlpatterns = [
  path('', views.index, name='index'),
  path('about', views.about, name='about'),
  path('faq', views.faq, name='faq'),
  path('unsubscribe', views.unsubscribe, name='unsub'),
  path('confirm_unsubscribe', views.confirm_unsubscribe, name='cm_unsub')
]