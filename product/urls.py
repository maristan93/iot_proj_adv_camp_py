from django.urls import path
from .views import result, list_items, coupon, survey, survey_list, coupon_list, coupon_check

urlpatterns = [
    path('result/', result, name='result'),
    path('survey/', survey, name='survey'),
    path('survey_list/', survey_list, name='survey_list'),
    path('list_items/', list_items, name='list_items'),
    path('coupon_list', coupon_list, name='coupon_list'),
    path('coupon/<int:item_pk>', coupon, name='coupon'),
    path('coupon_check/<int:item_pk>', coupon_check, name='coupon_check'),
]
