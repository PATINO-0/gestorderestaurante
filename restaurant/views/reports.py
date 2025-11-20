from django.views import View
from django.http import HttpResponse
from django.utils.timezone import now
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook

from restaurant.models import Order


class OrdersPDFReportView(View):
    def get(self, request):
        response = HttpResponse(content_type='application/pdf')
        filename = f"reporte_pedidos_{now().date()}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, height - 50, "Reporte de pedidos")

        p.setFont("Helvetica", 12)
        y = height - 80
        orders = Order.objects.all()[:100]
        for order in orders:
            text = f"#{order.id} - Mesa {order.table.number} - Total: ${order.total_amount} - Estado: {order.get_status_display()}"
            p.drawString(50, y, text)
            y -= 20
            if y < 50:
                p.showPage()
                y = height - 50

        p.showPage()
        p.save()
        return response


class OrdersExcelReportView(View):
    def get(self, request):
        wb = Workbook()
        ws = wb.active
        ws.title = "Pedidos"

        ws.append(["ID", "Mesa", "Cliente", "Estado", "Total", "Fecha"])

        for order in Order.objects.all()[:100]:
            ws.append([
                order.id,
                order.table.number,
                order.customer.username if order.customer else '',
                order.get_status_display(),
                float(order.total_amount),
                order.created_at.strftime('%Y-%m-%d %H:%M'),
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        filename = f"reporte_pedidos_{now().date()}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        wb.save(response)
        return response
