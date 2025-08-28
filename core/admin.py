# accounts/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # 리스트에 표시될 컬럼
    list_display = ("email", "nickname", "phone_number", "is_staff", "is_active")

    # 검색 조건
    search_fields = ("email", "nickname", "phone_number")

    # 필터 조건
    list_filter = ("is_staff", "is_active")

    # 읽기 전용 필드 (관리자 여부는 수정 불가)
    readonly_fields = ("is_staff",)

    # 필드 표시 순서 (어드민 페이지에서 표시될 필드들)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("개인 정보", {"fields": ("nickname", "phone_number")}),
        ("권한", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("중요한 날짜", {"fields": ("last_login", "date_joined")}),
    )

    # 유저 생성 시 사용하는 필드 (createsuperuser 할 때도 사용됨)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "nickname", "phone_number", "password1", "password2", "is_active"),
            },
        ),
    )

    ordering = ("email",)
