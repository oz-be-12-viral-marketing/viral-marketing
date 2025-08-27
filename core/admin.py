from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import NotRegistered

User = get_user_model()

try:
    admin.site.unregister(User)
except NotRegistered:
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 관리자 화면에서 보여줄 컬럼
    list_display = ("email", "nickname", "phone_number", "is_staff", "is_active")

    # 검색 기능 추가
    search_fields = ("email", "nickname", "phone_number")

    # 필터 기능 추가
    list_filter = ("is_staff", "is_active")

    # 읽기 전용 필드 (관리자가 수정 불가)
    readonly_fields = ("is_staff",)
