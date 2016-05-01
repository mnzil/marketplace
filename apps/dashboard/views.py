from datetime import timedelta
from decimal import Decimal as D
from django.db.models import Avg, Count, Sum
from django.utils.timezone import now
from oscar.apps.dashboard.views import IndexView as CoreIndexView
from oscar.core.loading import get_model
from oscar.core.compat import get_user_model


ConditionalOffer = get_model('offer', 'ConditionalOffer')
Voucher = get_model('voucher', 'Voucher')
Basket = get_model('basket', 'Basket')
StockAlert = get_model('partner', 'StockAlert')
Product = get_model('catalogue', 'Product')
Order = get_model('order', 'Order')
Line = get_model('order', 'Line')
User = get_user_model()


class IndexView(CoreIndexView):
    def get_active_site_offers(self):
        return ConditionalOffer.objects.filter(
            end_datetime__gt=now(),
            offer_type=ConditionalOffer.SITE,
            shop_id=self.request.shop_id)

    def get_stats(self):
        datetime_24hrs_ago = now() - timedelta(hours=24)

        orders = Order.objects.filter()
        orders_last_day = orders.filter(date_placed__gt=datetime_24hrs_ago)

        open_alerts = StockAlert.objects.filter(status=StockAlert.OPEN)
        closed_alerts = StockAlert.objects.filter(status=StockAlert.CLOSED)

        total_lines_last_day = Line.objects.filter(
            order__in=orders_last_day).count()
        stats = {
            'total_orders_last_day': orders_last_day.count(),
            'total_lines_last_day': total_lines_last_day,

            'average_order_costs': orders_last_day.aggregate(
                Avg('total_incl_tax')
            )['total_incl_tax__avg'] or D('0.00'),

            'total_revenue_last_day': orders_last_day.aggregate(
                Sum('total_incl_tax')
            )['total_incl_tax__sum'] or D('0.00'),

            'hourly_report_dict': self.get_hourly_report(hours=24),
            'total_customers_last_day': User.objects.filter(
                date_joined__gt=datetime_24hrs_ago,
            ).count(),

            'total_open_baskets_last_day': self.get_open_baskets({
                'date_created__gt': datetime_24hrs_ago
            }).count(),

            'total_products': Product.objects.filter(product_class__shop_id=self.request.shop_id).count(),
            'total_open_stock_alerts': open_alerts.count(),
            'total_closed_stock_alerts': closed_alerts.count(),

            'total_site_offers': self.get_active_site_offers().count(),
            'total_vouchers': self.get_active_vouchers().count(),
            'total_promotions': self.get_number_of_promotions(),

            'total_customers': User.objects.count(),
            'total_open_baskets': self.get_open_baskets().count(),
            'total_orders': orders.count(),
            'total_lines': Line.objects.filter(order__in=orders).count(),
            'total_revenue': orders.aggregate(
                Sum('total_incl_tax')
            )['total_incl_tax__sum'] or D('0.00'),

            'order_status_breakdown': orders.order_by(
                'status'
            ).values('status').annotate(freq=Count('id'))
        }
        return stats
