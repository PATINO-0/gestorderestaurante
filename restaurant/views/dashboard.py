from django.views.generic import TemplateView
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from accounts.models import User
from restaurant.models import Dish, Order, Reservation
from restaurant.permissions import RoleRequiredMixin


class DashboardView(RoleRequiredMixin, TemplateView):
    template_name = 'restaurant/dashboard.html'
    allowed_roles = ['ADMIN', 'WAITER']  # solo admin y mesero ven dashboard

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_orders = Order.objects.count()
        total_reservations = Reservation.objects.count()
        total_customers = User.objects.filter(role='CUSTOMER').count()

        # Top 5 platos más vendidos
        top_dishes = Dish.objects.annotate(
            total_sold=Sum('order_items__quantity')
        ).order_by('-total_sold')[:5]

        labels_dishes = [d.name for d in top_dishes]
        data_dishes = [d.total_sold or 0 for d in top_dishes]

        # Ingresos mensuales
        monthly_income = (
            Order.objects
            .filter(status__in=['SERVED', 'IN_PROGRESS', 'PENDING'])
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(total=Sum('total_amount'))
            .order_by('month')
        )

        labels_income = [m['month'].strftime('%Y-%m') for m in monthly_income]
        data_income = [float(m['total']) for m in monthly_income]

        context.update({
            'total_orders': total_orders,
            'total_reservations': total_reservations,
            'total_customers': total_customers,
            'labels_dishes': labels_dishes,
            'data_dishes': data_dishes,
            'labels_income': labels_income,
            'data_income': data_income,
        })
        return context
