from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from oscar.views import sort_queryset
from oscar.apps.dashboard.partners.views import \
    PartnerCreateView as CorePartnerCreateView, \
    PartnerManageView as CorePartnerManageView, \
    PartnerDeleteView as CorePartnerDeleteView, \
    PartnerUserCreateView as CorePartnerUserCreateView, \
    PartnerUserSelectView as CorePartnerUserSelectView, \
    PartnerUserLinkView as CorePartnerUserLinkView, \
    PartnerUserUnlinkView as CorePartnerUserUnlinkView, \
    PartnerUserUpdateView as CorePartnerUserUpdateView, \
    PartnerListView as CorePartnerListView
from oscar.core.compat import get_user_model
from oscar.core.loading import get_model

User = get_user_model()
Partner = get_model('partner', 'Partner')


class PartnerCreateView(CorePartnerCreateView):
    template_name = 'dashboard/partners/partner_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.shop_id = self.request.shop_id
        form.save()
        return super(PartnerCreateView, self).form_valid(form)


class PartnerListView(CorePartnerListView):
    def get_queryset(self):
        qs = self.model._default_manager.all().filter(
            shop_id=self.request.shop_id)
        qs = sort_queryset(qs, self.request, ['name'])
        self.description = _("All partners")
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Partners matching '%s'") % data['name']
            self.is_filtered = True

        return qs


class PartnerManageView(CorePartnerManageView):
    def get_object(self, queryset=None):
        self.partner = get_object_or_404(
            Partner,
            pk=self.kwargs['pk'],
            shop_id=self.request.shop_id)
        address = self.partner.primary_address
        if address is None:
            address = self.partner.addresses.model(partner=self.partner)
        return address


class PartnerDeleteView(CorePartnerDeleteView):
    def get_queryset(self):
        return Partner.objects.filter(shop_id=self.request.shop_id)


class PartnerUserCreateView(CorePartnerUserCreateView):
    def dispatch(self, request, *args, **kwargs):
        self.partner = get_object_or_404(
            Partner,
            pk=kwargs.get('partner_pk', None),
            shop_id=request.shop_id)
        return super(PartnerUserCreateView, self).dispatch(
            request, *args, **kwargs)


class PartnerUserSelectView(CorePartnerUserSelectView):
    def dispatch(self, request, *args, **kwargs):
        self.partner = get_object_or_404(
            Partner,
            pk=kwargs.get('partner_pk', None),
            shop_id=request.shop_id)
        return super(PartnerUserSelectView, self).dispatch(
            request, *args, **kwargs)


class PartnerUserLinkView(CorePartnerUserLinkView):
    def post(self, request, user_pk, partner_pk):
        user = get_object_or_404(User, pk=user_pk)
        name = user.get_full_name() or user.email
        partner = get_object_or_404(
            Partner,
            pk=partner_pk,
            shop_id=request.shop_id)
        if self.link_user(user, partner):
            messages.success(
                request,
                _("User '%(name)s' was linked to '%(partner_name)s'")
                % {'name': name, 'partner_name': partner.name})
        else:
            messages.info(
                request,
                _("User '%(name)s' is already linked to '%(partner_name)s'")
                % {'name': name, 'partner_name': partner.name})
        return redirect('dashboard:partner-manage', pk=partner_pk)


class PartnerUserUnlinkView(CorePartnerUserUnlinkView):
    def post(self, request, user_pk, partner_pk):
        user = get_object_or_404(User, pk=user_pk)
        name = user.get_full_name() or user.email
        partner = get_object_or_404(
            Partner,
            pk=partner_pk,
            shop_id=request.shop_id)
        if self.unlink_user(user, partner):
            msg = render_to_string(
                'dashboard/partners/messages/user_unlinked.html',
                {'user_name': name,
                 'partner_name': partner.name,
                 'user_pk': user_pk,
                 'partner_pk': partner_pk})
            messages.success(self.request, msg, extra_tags='safe noicon')
        else:
            messages.error(
                request,
                _("User '%(name)s' is not linked to '%(partner_name)s'") %
                {'name': name, 'partner_name': partner.name})
        return redirect('dashboard:partner-manage', pk=partner_pk)


class PartnerUserUpdateView(CorePartnerUserUpdateView):
    def get_object(self, queryset=None):
        self.partner = get_object_or_404(
            Partner,
            pk=self.kwargs['partner_pk'],
            shop_id=self.request.shop_id)
        return get_object_or_404(User,
                                 pk=self.kwargs['user_pk'],
                                 partners__pk=self.kwargs['partner_pk'])
