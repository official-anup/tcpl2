from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_view 

from django.urls import path
from TCPLapp import views
from django.conf.urls.static import static

from TCPLapp.forms import LoginForm,MyPasswordResetConfirm,MyPasswordResetForm,ChangePassword




urlpatterns = [
# path("admin/", admin.site.urls),
#path('', auth_view.LoginView.as_view(template_name="TCPLapp/login.html",authentication_form=LoginForm),name="login"),

path('', views.CustomLoginView.as_view(),name="login"),

path('registration/', views.CustomerRegistrationForm.as_view(),name="customerregistration"),
  
path('profile/', views.ProfileView.as_view(), name='profile'),

path('basemap/', views.basemap, name='basemap'),
   
path('user_details/', views.user_details, name='user_details'),

#change password
path('changepassword/',auth_view.PasswordChangeView.as_view(template_name="TCPLapp/changepassword.html",form_class=ChangePassword,success_url="/changepassworddone/"),name="changepassword"),
     
path('changepassworddone/',auth_view.PasswordChangeView.as_view(template_name="TCPLapp/changepassworddone.html"),name="changepassworddone"),


#forgot password
path("password-reset/",auth_view.PasswordResetView.as_view(template_name="TCPLapp/password_reset.html",form_class=MyPasswordResetForm),name="password_reset"),
    
path("password-reset/done/",auth_view.PasswordResetDoneView.as_view(template_name="TCPLapp/password_reset_done.html"),name="password_reset_done"),
    
path("password-reset-confirm/<uidb64>/<token>/",auth_view.PasswordResetConfirmView.as_view(template_name="TCPLapp/password_reset_confirm.html",form_class=MyPasswordResetConfirm),name="password_reset_confirm"),

path("password-reset-complete/",auth_view.PasswordResetCompleteView.as_view(template_name="TCPLapp/password_reset_complete.html"),name="password_reset_complete"),
    
#admin
path('admin123/',views.admin123,name='admin123'),

path('customer_details/<int:id>',views.customer_details,name='customer_details'),
     
#    path('user/', views.user,name='user'),
   
#    path('profile/', views.ProfileView.as_view(), name='profile'),
   
   
   
    
    
    #path('main/', views.main,name='main'),
    
    
    
    # path('user_details/<int:id>/', views.user_details,name='user_details'),
    
path('logout/',views.logout,name='logout'),
    
    # #path('coordinates/',views.coordinates,name='coordinates'),
    
path('index/', views.index,name='index'),
    
path('zoneDetail/', views.zoneDetail,name='zoneDetail'),

path('planSurvey/', views.planSurvey,name='planSurvey'),
    
path('mapCalculator/', views.mapCalculator,name='mapCalculator'),
    
path('upload_file_page/', views.upload_file_page, name='upload_file_page'),
   
path('upload_file/', views.upload_file, name='upload_file'),

#search urls
path('autocomplete/', views.autocomplete, name='autocomplete'),
    
path('searchOnClick/', views.searchOnClick, name='searchOnClick'),
    
path('Out_table/', views.Out_table, name='Out_table'),
#bookmark   
path('save-location/', views.save_location, name='save_location'),
    
path('get-locations/', views.get_locations, name='get_locations'),
    
path('delete-location/', views.delete_location, name='delete_location'),

#payment

path('before_payment/', views.before_payment, name='before_payment'),    
path('paymentdone/', views.payment_done, name='paymentdone'),

#search coordinates

#path('Search_coordinates/', views.Search_coordinates, name='Search_coordinates'),

#path('selected_data/', views.selected_data, name='selected_data'),

path('locations/', views.locations, name='locations'),

path('getInfoValues/', views.getInfoValues, name='getInfoValues'),

path('user_details/', views.user_details, name='user_details'),

path('Queryform/', views.Queryform, name='Queryform'),



    
   # path('fetch_searchdata/<int:id>/',views.fetch_searchdata, name='fetch_searchdata')
   
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
