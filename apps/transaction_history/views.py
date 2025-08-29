from rest_framework import viewsets, permissions, serializers
from django_filters import rest_framework as filters
from .models import TransactionHistory
from .serializers import TransactionHistorySerializer

class TransactionHistoryFilter(filters.FilterSet):
    """
    Filter for TransactionHistory
    """
    transaction_type = filters.CharFilter(field_name='transaction_type', lookup_expr='iexact')
    amount = filters.NumberFilter(field_name='amount', lookup_expr='exact')
    amount__gt = filters.NumberFilter(field_name='amount', lookup_expr='gt')
    amount__lt = filters.NumberFilter(field_name='amount', lookup_expr='lt')

    class Meta:
        model = TransactionHistory
        fields = ['transaction_type', 'amount', 'amount__gt', 'amount__lt']

class TransactionHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transaction history to be viewed or edited.
    """
    serializer_class = TransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TransactionHistoryFilter

    def get_queryset(self):
        """
        This view should return a list of all the transaction histories
        for the accounts owned by the currently authenticated user.
        """
        return TransactionHistory.objects.filter(account__user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new transaction history and update the account balance.
        """
        # Note: This is a simplified example. In a real-world scenario,
        # you would want to handle this within a database transaction
        # to ensure data integrity.
        account = serializer.validated_data['account']
        amount = serializer.validated_data['amount']
        transaction_type = serializer.validated_data['transaction_type']

        if transaction_type == 'DEPOSIT':
            account.balance += amount
        elif transaction_type == 'WITHDRAW':
            if account.balance < amount:
                raise serializers.ValidationError("Insufficient funds.")
            account.balance -= amount
        
        account.save()
        serializer.save(balance_after=account.balance)