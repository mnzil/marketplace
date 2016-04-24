from oscar.apps.dashboard.offers.views import \
    OfferListView as CoreOfferListView


class OfferListView(CoreOfferListView):
    def get_queryset(self):
        qs = self.model._default_manager.exclude(
            offer_type=ConditionalOffer.VOUCHER)
        qs = sort_queryset(qs, self.request,
                           ['name', 'start_datetime', 'end_datetime',
                            'num_applications', 'total_discount'])

        self.description = _("All offers")
        self.is_filtered = False
        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return qs

        data = self.form.cleaned_data

        if data['name']:
            qs = qs.filter(name__icontains=data['name'])
            self.description = _("Offers matching '%s'") % data['name']
            self.is_filtered = True
        if data['is_active']:
            self.is_filtered = True
            today = timezone.now()
            qs = qs.filter(start_datetime__lte=today, end_datetime__gte=today)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super(OfferListView, self).get_context_data(**kwargs)
        ctx['queryset_description'] = self.description
        ctx['form'] = self.form
        ctx['is_filtered'] = self.is_filtered
        return ctx
