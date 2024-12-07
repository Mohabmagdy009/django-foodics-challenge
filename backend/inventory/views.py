# region Imports
from utils.baseclasses.base_views import CustomResponseViewSet
from .models import Order
from .serializers import OrderSerializer
from utils.endpointhandling.custom_django_permissions import CustomDjangoModelPermissions
# endregion


# region View Sets
class OrderViewSet(CustomResponseViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CustomDjangoModelPermissions]
# endregion
