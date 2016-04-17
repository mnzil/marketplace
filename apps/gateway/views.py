import logging

from django.views import generic
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django import http
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth.models import Permission

from . import forms
from oscar.apps.customer.forms import generate_username
from oscar.core.loading import get_model

Partner = get_model('partner', 'Partner')
Shop = get_model('partner', 'Shop')

logger = logging.getLogger('gateway')


class GatewayView(generic.FormView):
    template_name = 'gateway/form.html'
    form_class = forms.GatewayForm

    def form_valid(self, form):
        code = form.cleaned_data['shop_name']
        email = form.cleaned_data['email']
        full_name = form.cleaned_data['full_name']
        username = generate_username()
        password = generate_username()

        user = self.create_dashboard_user(username, email, password, full_name, code)
        self.send_confirmation_email(email, user, password)
        logger.info("Created dashboard user #%d for %s",
                    user.id, email)

        messages.success(
            self.request,
            "The credentials for a dashboard user have been sent to %s" % email)
        return http.HttpResponseRedirect(reverse('gateway'))

    def create_dashboard_user(self, username, email, password, full_name, title):
        user = User.objects.create_user(username, email, password)
        permission = Permission.objects.get(name='Can access dashboard')
        user.user_permissions.add(permission)
        user.is_staff = False
        user.is_active = False

        try:
            latest_shop = int(Shop.objects.latest('id')['id'])
        except:
            latest_shop = 0
        shop = Shop(latest_shop + 1, title=title)
        shop.save()

        try:
            latest_partner = Partner.objects.latest('id')['id']
        except:
            latest_partner = 0
        partner = Partner(latest_partner + 1, name=full_name)

        user.save()
        partner.save()

        partner.users.add(user)
        partner.shop.add(shop)
        return user

    def send_confirmation_email(self, email, user, password):
        msg = get_template('gateway/email.txt').render(Context({
            'email': user.email,
            'password': password
        }))
        send_mail('Dashboard Access to Django MarketPlace',
                  msg, 'no-reply@djmarketplace.com',
                  [email])
