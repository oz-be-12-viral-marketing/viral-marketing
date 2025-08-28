from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ('user', 'account_number', 'balance', 'created_at', 'updated_at')
