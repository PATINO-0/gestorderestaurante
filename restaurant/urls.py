from django.urls import path
from .views import (
    DashboardView,
    DishListView, DishCreateView, DishUpdateView, DishDeleteView,
    ReservationListView, ReservationCreateView, ReservationUpdateView, ReservationDeleteView,
    OrderListView, OrderCreateView, OrderUpdateView, OrderDeleteView,
    OrdersPDFReportView, OrdersExcelReportView,
    TableListView, TableCreateView, TableUpdateView, TableDeleteView,
    IngredientListView, IngredientCreateView, IngredientUpdateView, IngredientDeleteView,
)

app_name = 'restaurant'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    # Platos
    path('dishes/', DishListView.as_view(), name='dish_list'),
    path('dishes/create/', DishCreateView.as_view(), name='dish_create'),
    path('dishes/<int:pk>/edit/', DishUpdateView.as_view(), name='dish_edit'),
    path('dishes/<int:pk>/delete/', DishDeleteView.as_view(), name='dish_delete'),

    # Ingredientes
    path('ingredients/', IngredientListView.as_view(), name='ingredient_list'),
    path('ingredients/create/', IngredientCreateView.as_view(), name='ingredient_create'),
    path('ingredients/<int:pk>/edit/', IngredientUpdateView.as_view(), name='ingredient_edit'),
    path('ingredients/<int:pk>/delete/', IngredientDeleteView.as_view(), name='ingredient_delete'),

    # Mesas
    path('tables/', TableListView.as_view(), name='table_list'),
    path('tables/create/', TableCreateView.as_view(), name='table_create'),
    path('tables/<int:pk>/edit/', TableUpdateView.as_view(), name='table_edit'),
    path('tables/<int:pk>/delete/', TableDeleteView.as_view(), name='table_delete'),

    # Reservas
    path('reservations/', ReservationListView.as_view(), name='reservation_list'),
    path('reservations/create/', ReservationCreateView.as_view(), name='reservation_create'),
    path('reservations/<int:pk>/edit/', ReservationUpdateView.as_view(), name='reservation_edit'),
    path('reservations/<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation_delete'),

    # Pedidos
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/edit/', OrderUpdateView.as_view(), name='order_edit'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),

    # Reportes
    path('reports/orders/pdf/', OrdersPDFReportView.as_view(), name='orders_pdf'),
    path('reports/orders/excel/', OrdersExcelReportView.as_view(), name='orders_excel'),
]
