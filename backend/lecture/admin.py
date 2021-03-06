from django.contrib import admin
from .models import Lecture, Category, Siteinfo, Profile  # 모델에서 Resource를 불러온다

# 출력할 ResourceAdmin 클래스를 만든다
class LectureAdmin(admin.ModelAdmin):
    list_display = ['lectureidx', 'lecturename']
    search_fields = ['lectureidx']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['categoryidx', 'categoryname']
    search_fields = ['categoryidx']

class SiteinfoAdmin(admin.ModelAdmin):
    list_display = ['siteidx', 'sitename']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['userinfo', 'name']


# 클래스를 어드민 사이트에 등록한다.
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Siteinfo, SiteinfoAdmin)
admin.site.register(Profile, ProfileAdmin)