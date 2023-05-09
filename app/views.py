from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Memo
from .serializers import MemoSerializer

class MemoViewSet(viewsets.ModelViewSet):
    serializer_class = MemoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Memo.objects.filter(user=self.request.user)
