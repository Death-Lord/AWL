from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('display',views.display_users, name = 'display_users'),
    path('display/<int:user_id>',views.display_specific_users, name = 'display_specific_users'),
    path('display_detail/<int:user_id>',views.display_detail, name = 'display_detail'),
    path('register', views.register_user, name='register_user'),
    path('login', views.login_user, name = 'login_user'),
    path('validate_registeration/<str:first_name>/<str:last_name>/<str:email>/<slug:user_name>/<slug:password>', views.validate_registeration, name = 'validate_registeration'),
    path('logout', views.logout, name = 'logout'),
    path('forgot_password', views.forgot_password, name = 'forgot_password'),
    path('reset_password/<int:user_id>', views.reset_password, name = 'reset_password'),
    path('profile_pic/<int:user_id>', views.profile_pic, name = 'profile_pic'),
    path('profile_pic_upload/<int:user_id>', views.profile_pic_upload, name = 'profile_pic_upload'),
    path('account_details/<int:user_id>', views.account_details, name = 'account_details'),
    path('soundmeter',views.soundmeter, name = 'soundmeter'),
    path('submit_post', views.submit_post, name = 'submit_post'),
    path('forum', views.forum_portal, name = 'forum'),
    path('chatbot', views.chatbot, name = 'chatbot'),
    path('air_api', views.air_api, name = 'air_api'),
    path('upload_image', views.upload_image, name = 'upload_image'),
    path('analyse_uploaded_image/<str:image>', views.analyse_uploaded_image, name = 'analyse_uploaded_image'),
    path('vehicle', views.vehicles, name='vehicle'),
]
