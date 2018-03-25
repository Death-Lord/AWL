from django.contrib import admin
# Register your models here.
from .models import users,forum, analyse_image, chatbot_save
admin.site.register(users)
admin.site.register(forum)
admin.site.register(analyse_image)
admin.site.register(chatbot_save)
