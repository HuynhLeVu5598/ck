
from django.urls import path
from .views import home,user_login,user_logout,user_register
from django.conf import settings
from django.conf.urls.static import static

from .views import pdf_view,thietlap,post_order,order_detail,upload_excel,sno_list,thietlap_detail,thietlap_sno,request_list,delete_request
from .views import giacong,soyeucau_detail, giacong_detail, thongtingiacong,sno_detail_edit_save,sno_kochuan_list,kiemtratuchu,tuchu_detail
from .views import save_kiemtratuchu, baocaohoatdong, save_baocaohoatdong,get_file_drawing
from .views import nhanvien,post_test,a,b

from .views import ClearOrderView,ClearOrderResultView,ClearSnoView,ClearSnoResultView,ClearProcessingTimeView,ClearProcessingTimeResultView
from .views import SnoDetailView,SnoDetailView2,RequestDetailView,EditRequestDetailView,SnoEditDetailView


urlpatterns = [
    path('', sno_list, name='home'),
    path('skochuan', sno_kochuan_list, name='s_khong_chuan'),
    
    path('orders/<str:order_sno>/', order_detail, name='order_detail'),
    # path('types/<str:order_type_s>/', sno_list, name='sno_list'),

    path('thietlap/', thietlap, name='thietlap'),
    path('thietlap_sno/', thietlap_sno, name='thietlap_sno'),
    path('nhanvien/', nhanvien, name='nhanvien'),
    path('thietlap_detail/', thietlap_detail, name='thietlap_detail'),

    path('post_order/', post_order, name='post_order'),
 

    
    path('a/', a, name='a'),
    path('b/', b, name='b'),


    # path('post_test/', post_test, name='post_test'),

    

    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', user_register, name='user_register'),

    path('pdf/', pdf_view, name='pdf_view'),
    path('upload/', upload_excel, name='upload_excel'),


    path('clear_order/', ClearOrderView.as_view(), name='clear_order'),  
    path('clear_order/result/', ClearOrderResultView.as_view(), name='clear_order_result'),  
    path('clear_sno/', ClearSnoView.as_view(), name='clear_sno'),  
    path('clear_sno/result/', ClearSnoResultView.as_view(), name='clear_sno_result'), 
    path('clear_processingtime/', ClearProcessingTimeView.as_view(), name='clear_processingtime'),  
    path('clear_processingtime/result/', ClearProcessingTimeResultView.as_view(), name='clear_processingtime_result'),

    path('sno/<str:sno>/', SnoDetailView.as_view(), name='sno_detail'),
    path('sno/<str:sno>/edit', SnoEditDetailView.as_view(), name='sno_detail_edit'),
   path('sno_detail_edit_save/', sno_detail_edit_save, name='sno_detail_edit_save'),
   
    # path('sno/<str:sno>/<str:material>/', SnoDetailView2.as_view(), name='sno_detail2'),

    #  path('save_request_info/', save_request_info, name='save_request_info'),
    path('request_list/', request_list, name='request_list'),
    path('request_detail/<int:pk>/', RequestDetailView.as_view(), name='request_detail'),
    # path('edit_request/<int:pk>/', EditRequestView.as_view(), name='edit_request'),  # Add/EditRequestView
    path('delete_request/<int:request_id>/', delete_request, name='delete_request'),

    path('edit_request_detail/<int:pk>/', EditRequestDetailView.as_view(), name='edit_request_detail'),
    path('giacong/', giacong, name='giacong'),
    path('soyeucau/<str:request_number>/', soyeucau_detail, name='soyeucau_detail'),
    path('thongtingiacong/', thongtingiacong, name='thongtingiacong'),

    path('thongtingiacong/<str:request_number>/', giacong_detail, name='giacong_detail'),
    path('kiemtratuchu/', kiemtratuchu, name='kiemtratuchu'),
    path('baocaohoatdong/', baocaohoatdong, name='baocaohoatdong'),
    path('save_baocaohoatdong/', save_baocaohoatdong, name='save_baocaohoatdong'),
    # path('baocaohoatdong/', a, name='baocaohoatdong'),
    # path('save_baocaohoatdong/', a, name='save_baocaohoatdong'),

    path('kiemtratuchu/<str:request_number>/', tuchu_detail, name='tuchu_detail'),
    path('save_kiemtratuchu/', save_kiemtratuchu, name='save_kiemtratuchu'),

    path('get_file_drawing/', get_file_drawing, name='save_kiemtratuchu'),


]



# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)