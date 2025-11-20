from .dashboard import DashboardView
from .dishes import (
    DishListView, DishCreateView, DishUpdateView, DishDeleteView
)
from .reservations import (
    ReservationListView, ReservationCreateView, ReservationUpdateView, ReservationDeleteView
)
from .orders import (
    OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView
)
from .reports import OrdersPDFReportView, OrdersExcelReportView
from .tables import (
    TableListView, TableCreateView, TableUpdateView, TableDeleteView
)
from .ingredients import (
    IngredientListView, IngredientCreateView, IngredientUpdateView, IngredientDeleteView
)
