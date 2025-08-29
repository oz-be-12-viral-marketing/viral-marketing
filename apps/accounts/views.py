from rest_framework import viewsets, permissions
from .models import Account
from .serializers import AccountSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status # Import status for examples

@extend_schema(
    description="API for managing user accounts. Provides CRUD operations for accounts associated with the authenticated user.",
    parameters=[
        OpenApiParameter(
            name='user',
            type=str,
            location=OpenApiParameter.QUERY,
            description='Filter accounts by user ID (only accessible for authenticated user\'s own accounts).',
            required=False,
        ),
    ],
    responses={
        status.HTTP_200_OK: AccountSerializer,
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication credentials were not provided."},
        status.HTTP_403_FORBIDDEN: {"description": "You do not have permission to perform this action."},
    },
    examples=[
        OpenApiExample(
            'List Accounts Example',
            summary='Example of listing accounts',
            description='This example shows how to retrieve a list of accounts for the authenticated user.',
            value=[
                {
                    "id": 1,
                    "user": 1,
                    "account_number": "1234567890",
                    "bank_code": "004",
                    "account_type": "CHECKING",
                    "balance": "1000.00",
                    "currency": "KR"
                },
                {
                    "id": 2,
                    "user": 1,
                    "account_number": "0987654321",
                    "bank_code": "088",
                    "account_type": "SAVING",
                    "balance": "5000.00",
                    "currency": "US"
                }
            ],
            request_only=False,
            response_only=True,
        ),
    ]
)
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

    @extend_schema(
        summary="Create a new account",
        description="Creates a new bank account for the authenticated user. The account number and initial balance are automatically generated.",
        request=AccountSerializer,
        responses={
            status.HTTP_201_CREATED: AccountSerializer,
            status.HTTP_400_BAD_REQUEST: {"description": "Invalid input data."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Authentication credentials were not provided."},
        },
        examples=[
            OpenApiExample(
                'Create Account Request',
                summary='Example request for creating an account',
                description='This example shows the data required to create a new account.',
                value={
                    "bank_code": "004",
                    "account_type": "CHECKING",
                    "currency": "KR"
                },
                request_only=True,
            ),
            OpenApiExample(
                'Create Account Response',
                summary='Example response for creating an account',
                description='This example shows the response after successfully creating an account.',
                value={
                    "id": 3,
                    "user": 1,
                    "account_number": "AUTO_GENERATED_123",
                    "bank_code": "004",
                    "account_type": "CHECKING",
                    "balance": "0.00",
                    "currency": "KR"
                },
                response_only=True,
            ),
        ]
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a specific account",
        description="Retrieves the details of a single account by its ID, belonging to the authenticated user.",
        responses={
            status.HTTP_200_OK: AccountSerializer,
            status.HTTP_404_NOT_FOUND: {"description": "Account not found."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Authentication credentials were not provided."},
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update an existing account",
        description="Updates the details of an existing account. Only bank_code, account_type, and currency can be updated.",
        request=AccountSerializer,
        responses={
            status.HTTP_200_OK: AccountSerializer,
            status.HTTP_400_BAD_REQUEST: {"description": "Invalid input data."},
            status.HTTP_404_NOT_FOUND: {"description": "Account not found."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Authentication credentials were not provided."},
        },
        examples=[
            OpenApiExample(
                'Update Account Request',
                summary='Example request for updating an account',
                description='This example shows the data required to update an account.',
                value={
                    "bank_code": "088",
                    "account_type": "SAVING",
                    "currency": "US"
                },
                request_only=True,
            ),
            OpenApiExample(
                'Update Account Response',
                summary='Example response for updating an account',
                description='This example shows the response after successfully updating an account.',
                value={
                    "id": 1,
                    "user": 1,
                    "account_number": "1234567890",
                    "bank_code": "088",
                    "account_type": "SAVING",
                    "balance": "1000.00",
                    "currency": "US"
                },
                response_only=True,
            ),
        ]
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update an existing account",
        description="Partially updates the details of an existing account. Only bank_code, account_type, and currency can be updated.",
        request=AccountSerializer(partial=True),
        responses={
            status.HTTP_200_OK: AccountSerializer,
            status.HTTP_400_BAD_REQUEST: {"description": "Invalid input data."},
            status.HTTP_404_NOT_FOUND: {"description": "Account not found."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Authentication credentials were not provided."},
        },
        examples=[
            OpenApiExample(
                'Partial Update Account Request',
                summary='Example request for partially updating an account',
                description='This example shows the data required to partially update an account.',
                value={
                    "currency": "JP"
                },
                request_only=True,
            ),
            OpenApiExample(
                'Partial Update Account Response',
                summary='Example response for partially updating an account',
                description='This example shows the response after successfully partially updating an account.',
                value={
                    "id": 1,
                    "user": 1,
                    "account_number": "1234567890",
                    "bank_code": "004",
                    "account_type": "CHECKING",
                    "balance": "1000.00",
                    "currency": "JP"
                },
                response_only=True,
            ),
        ]
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an account",
        description="Deletes an account belonging to the authenticated user.",
        responses={
            status.HTTP_204_NO_CONTENT: {"description": "Account successfully deleted."},
            status.HTTP_404_NOT_FOUND: {"description": "Account not found."},
            status.HTTP_401_UNAUTHORIZED: {"description": "Authentication credentials were not provided."},
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
