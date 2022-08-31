from django.contrib import admin
from .models import Peoples, Dolzhnost, Otpuska, Tabel, Proba,  Programm, Otdels, Progconnect


class ListAdmin(admin.ModelAdmin):
    list_display = ('id','familia', 'name', 'female',  'dolzhnost',  'otdel_people', 'photo')
    #filter_horizontal = ('programma',)



class ListAdminDolzhnost(admin.ModelAdmin):
    list_display = ('id','titleDolzhnost')

class ListAdminOtdels(admin.ModelAdmin):
    list_display = ('id','myotdel')

class ListAdminProgramm(admin.ModelAdmin):
    list_display = ('id','name_programm')

class ListAdminProgconnect(admin.ModelAdmin):
    list_display = ('id','prog', 'peop')



# class ListAdminDescribe(admin.ModelAdmin):
#     list_display = ('id','obosnovanie')

class ListAdminOtpusk(admin.ModelAdmin):
    list_display = ('id', 'person', 'title_otpusk', 'nachOtpusk', 'kolvoDney', 'konecOtpusk', 'zayvlenie')


class ListAdminTabel(admin.ModelAdmin):
    list_display = ('id','dataTabel', 'workTime', 'man', 'primechanie')

class ListAdminProba(admin.ModelAdmin):
    list_display = ('name','sename', 'age', 'e_mail', 'data')

admin.site.register(Peoples, ListAdmin)
admin.site.register(Dolzhnost, ListAdminDolzhnost)
admin.site.register(Otpuska, ListAdminOtpusk)

admin.site.register(Tabel, ListAdminTabel)
admin.site.register(Otdels, ListAdminOtdels)
admin.site.register(Programm, ListAdminProgramm)
admin.site.register(Progconnect, ListAdminProgconnect)


admin.site.register(Proba, ListAdminProba)
# Register your models here.
