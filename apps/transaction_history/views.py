from django_filters import rest_framework as filters
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status  # Import status for examples
from rest_framework import permissions, serializers, viewsets

from .models import TransactionHistory
from .serializers import TransactionHistorySerializer


class TransactionHistoryFilter(filters.FilterSet):
    """
    Filter for TransactionHistory
    """

    transaction_type = filters.CharFilter(field_name="transaction_type", lookup_expr="iexact")
    amount = filters.NumberFilter(field_name="amount", lookup_expr="exact")
    amount__gt = filters.NumberFilter(field_name="amount", lookup_expr="gt")
    amount__lt = filters.NumberFilter(field_name="amount", lookup_expr="lt")

    class Meta:
        model = TransactionHistory
        fields = ["transaction_type", "amount", "amount__gt", "amount__lt"]


@extend_schema(
    description="API for managing transaction history. Provides CRUD operations for transactions associated with the authenticated user's accounts.",
    parameters=[
        OpenApiParameter(
            name="transaction_type",
            type=str,
            location=OpenApiParameter.QUERY,
            description="Filter transactions by type (e.g., DEPOSIT, WITHDRAW).",
            required=False,
        ),
        OpenApiParameter(
            name="amount",
            type=float,
            location=OpenApiParameter.QUERY,
            description="Filter transactions by exact amount.",
            required=False,
        ),
        OpenApiParameter(
            name="amount__gt",
            type=float,
            location=OpenApiParameter.QUERY,
            description="Filter transactions by amount greater than.",
            required=False,
        ),
        OpenApiParameter(
            name="amount__lt",
            type=float,
            location=OpenApiParameter.QUERY,
            description="Filter transactions by amount less than.",
            required=False,
        ),
    ],
    responses={
        status.HTTP_200_OK: TransactionHistorySerializer,
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication credentials were not provided."},
        status.HTTP_403_FORBIDDEN: {"description": "You do not have permission to perform this action."},
    },
    examples=[
        OpenApiExample(
            "List Transactions Example",
            summary="Example of listing transactions",
            description="This example shows how to retrieve a list of transactions for the authenticated user's accounts.",
            value=[
                {
                    "id": 1,
                    "account": 1,
                    "transaction_type": "DEPOSIT",
                    "amount": "100.00",
                    "balance_after": "1100.00",
                    "transaction_detail": "Initial deposit",
                    "transaction_method": "ATM",
                },
                {
                    "id": 2,
                    "account": 1,
                    "transaction_type": "WITHDRAW",
                    "amount": "50.00",
                    "balance_after": "1050.00",
                    "transaction_detail": "Coffee",
                    "transaction_method": "CARD",
                },
            ],
            request_only=False,
            response_only=True,
        ),
    ],
)
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
        account = serializer.validated_data["account"]
        amount = serializer.validated_data["amount"]
        transaction_type = serializer.validated_data["transaction_type"]

        if transaction_type == "DEPOSIT":
            account.balance += amount
        elif transaction_type == "WITHDRAW":
            if account.balance < amount:
                raise serializers.ValidationError("Insufficient funds.")
            account.balance -= amount

        account.save()
        serializer.save(balance_after=account.balance)

    @extend_schema(
        summary="Create a new transaction",
        description="Creates a new transaction (deposit or withdrawal) for a specified account. Updates the account balance accordingly.",
        request=TransactionHistorySerializer,
        responses={
            status.HTTP_201_CREATED: TransactionHistorySerializer,
            status.HTTP_400_BAD_REQUEST: {"description": "Invalid input data or insufficient funds."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Authentication credentials were not provided."},
        },
        examples=[
            OpenApiExample(
                "Create Deposit Request",
                summary="Example request for creating a deposit",
                description="This example shows the data required to create a deposit transaction.",
                value={
                    "account": 1,
                    "transaction_type": "DEPOSIT",
                    "amount": "100.00",
                    "transaction_detail": "Salary",
                    "transaction_method": "TRANSFER",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Create Withdrawal Request",
                summary="Example request for creating a withdrawal",
                description="This example shows the data required to create a withdrawal transaction.",
                value={
                    "account": 1,
                    "transaction_type": "WITHDRAW",
                    "amount": "50.00",
                    "transaction_detail": "Groceries",
                    "transaction_method": "CARD",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Create Transaction Response",
                summary="Example response for creating a transaction",
                description="This example shows the response after successfully creating a transaction.",
                value={
                    "id": 3,
                    "account": 1,
                    "transaction_type": "DEPOSIT",
                    "amount": "100.00",
                    "balance_after": "1200.00",
                    "transaction_detail": "Salary",
                    "transaction_method": "TRANSFER",
                },
                response_only=True,
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a specific transaction",
        description="Retrieves the details of a single transaction by its ID, belonging to the authenticated user's accounts.",
        responses={
            status.HTTP_200_OK: TransactionHistorySerializer,
            status.HTTP_404_NOT_FOUND: {"description": "Transaction not found."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Authentication credentials were not provided."},
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update an existing transaction (Not typically allowed for history)",
        description="Updates the details of an existing transaction. Note: Transaction history is typically immutable. Use with caution.",
        request=TransactionHistorySerializer,
        responses={
            status.HTTP_200_OK: TransactionHistorySerializer,
            status.HTTP_400_BAD_REQUEST: {"description": "Invalid input data."},
            status.HTTP_404_NOT_FOUND: {"description": "Transaction not found."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Authentication credentials were not provided."},
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update an existing transaction (Not typically allowed for history)",
        description="Partially updates the details of an existing transaction. Note: Transaction history is typically immutable. Use with caution.",
        request=TransactionHistorySerializer(partial=True),
        responses={
            status.HTTP_200_OK: TransactionHistorySerializer,
            status.HTTP_400_BAD_REQUEST: {"description": "Invalid input data."},
            status.HTTP_404_NOT_FOUND: {"description": "Transaction not found."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Authentication credentials were not provided."},
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a transaction (Not typically allowed for history)",
        description="Deletes a transaction belonging to the authenticated user's accounts. Note: Transaction history is typically immutable. Use with caution.",
        responses={
            status.HTTP_204_NO_CONTENT: {"description": "Transaction successfully deleted."},
            status.HTTP_404_NOT_FOUND: {"description": "Transaction not found."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Authentication credentials were not provided."},
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
