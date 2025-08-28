from rest_framework import viewsets, permissions
from .models import Account
from .serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the accounts
        for the currently authenticated user.
        """
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Associate the user with the account.
        """
        serializer.save(user=self.request.user)