from django.shortcuts import get_object_or_404
from oscar.apps.dashboard.offers.views import \
    OfferListView as CoreOfferListView, \
    OfferBenefitView as CoreOfferBenefitView, \
    OfferConditionView as CoreOfferConditionView, \
    OfferWizardStepView as CoreOfferWizardStepView, \
    OfferRestrictionsView as CoreOfferRestrictionsView, \
    OfferDetailView as CoreOfferDetailView, \
    OfferMetaDataView as CoreOfferMetaDataView, \
    OfferDeleteView as CoreOfferDeleteView
from oscar.core.loading import get_model

ConditionalOffer = get_model('offer', 'ConditionalOffer')


class OfferListView(CoreOfferListView):
    def get_queryset(self):
        return super(OfferListView, self).get_queryset().filter(
            shop_id=self.request.shop_id)


class OfferWizardStepView(CoreOfferWizardStepView):
    def dispatch(self, request, *args, **kwargs):
        if self.update:
            print self.request.shop_id
            self.offer = get_object_or_404(
                ConditionalOffer,
                pk=kwargs['pk'],
                shop_id=self.request.shop_id)
        return super(OfferWizardStepView, self).dispatch(request, *args,
                                                         **kwargs)

    def save_offer(self, offer):
        offer.shop_id = self.request.shop_id
        return super(OfferWizardStepView, self).save_offer(offer)


class OfferBenefitView(OfferWizardStepView, CoreOfferBenefitView):
    def get_context_data(self, **kwargs):
        ctx = super(OfferBenefitView, self).get_context_data(**kwargs)
        ctx['form'] = self.form_class(shop_id=self.request.shop_id)
        return ctx


class OfferConditionView(OfferWizardStepView, CoreOfferConditionView):
    def get_context_data(self, **kwargs):
        ctx = super(OfferConditionView, self).get_context_data(**kwargs)
        ctx['form'] = self.form_class(shop_id=self.request.shop_id)
        return ctx


class OfferRestrictionsView(OfferWizardStepView, CoreOfferRestrictionsView):
    pass


class OfferMetaDataView(OfferWizardStepView, CoreOfferMetaDataView):
    pass


class OfferDetailView(CoreOfferDetailView):
    def dispatch(self, request, *args, **kwargs):
        self.offer = get_object_or_404(
            ConditionalOffer,
            pk=kwargs['pk'],
            shop_id=self.request.shop_id)
        return super(OfferDetailView, self).dispatch(request, *args, **kwargs)


class OfferDeleteView(CoreOfferDeleteView):
    def get_object(self):
        self.offer = get_object_or_404(
            ConditionalOffer,
            pk=self.kwargs.get('pk', None),
            shop_id=self.request.shop_id)
        return super(OfferDeleteView, self).get_object()
