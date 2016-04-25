from oscar.apps.dashboard.offers.forms import \
    BenefitForm as CoreBenefitForm, \
    ConditionForm as CoreConditionForm
from oscar.core.loading import get_model

Benefit = get_model('offer', 'Benefit')
Range = get_model('offer', 'Range')


class BenefitForm(CoreBenefitForm):
    def __init__(self, *args, **kwargs):
        shop_id = kwargs.pop('shop_id', None)
        super(BenefitForm, self).__init__(*args, **kwargs)
        if shop_id is not None and self.fields:
            self.fields['range'].queryset = Range.objects.filter(
                 shop_id=shop_id)


class ConditionForm(CoreConditionForm):
    def __init__(self, *args, **kwargs):
        shop_id = kwargs.pop('shop_id', None)
        super(ConditionForm, self).__init__(*args, **kwargs)
        if shop_id is not None and self.fields:
            self.fields['range'].queryset = Range.objects.filter(
                 shop_id=shop_id)
