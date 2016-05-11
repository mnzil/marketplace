from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView, View

from oscar.apps.catalogue.reviews.signals import review_added
from oscar.core.loading import get_classes, get_model
from oscar.core.utils import redirect_to_referrer

ShopReviewForm, VoteForm, SortReviewsForm = get_classes(
    'partner.shopreviews.forms',
    ['ShopReviewForm', 'VoteForm', 'SortReviewsForm'])
Vote = get_model('reviews', 'vote')
ShopReview = get_model('shopreviews', 'ShopReview')
Shop = get_model('partner', 'Shop')
Product = get_model('catalogue', 'Product')


class CreateShopReview(CreateView):
    template_name = "partner/shopreviews/review_form.html"
    model = ShopReview
    shop_model = Shop
    form_class = ShopReviewForm
    view_signal = review_added

    def dispatch(self, request, *args, **kwargs):
        self.shop = get_object_or_404(
            self.shop_model, pk=kwargs['shop_pk'])
        # check permission to leave review
        if not self.shop.is_review_permitted(request.user):
            if self.shop.has_review_by(request.user):
                message = _("You have already reviewed this shop!")
            else:
                message = _("You can't leave a review for this shop.")
            messages.warning(self.request, message)
            return redirect(self.shop.get_absolute_url())

        self.products = Product.objects.filter(product_class__shop_id=kwargs['shop_pk'])
        print self.shop.shopreviews.filter(status=1)
        return super(CreateShopReview, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateShopReview, self).get_context_data(**kwargs)
        context['shop'] = self.shop
        context['products'] = self.products
        return context

    def get_form_kwargs(self):
        kwargs = super(CreateShopReview, self).get_form_kwargs()
        kwargs['shop'] = self.shop
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super(CreateShopReview, self).form_valid(form)
        self.send_signal(self.request, response, self.object)
        return response

    def get_success_url(self):
        messages.success(
            self.request, _("Thank you for reviewing this shop"))
        return self.shop.get_absolute_url()

    def send_signal(self, request, response, review):
        self.view_signal.send(sender=self, review=review, user=request.user,
                              request=request, response=response)


class ShopReviewDetail(DetailView):
    template_name = "partner/shopreviews/review_detail.html"
    context_object_name = 'review'
    model = ShopReview

    def get_context_data(self, **kwargs):
        context = super(ShopReviewDetail, self).get_context_data(**kwargs)
        context['shop'] = get_object_or_404(
            Shop, pk=self.kwargs['shop_pk'])
        return context


class AddVoteView(View):
    """
    Simple view for voting on a review.

    We use the URL path to determine the shop and review and use a 'delta'
    POST variable to indicate it the vote is up or down.
    """

    def post(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, pk=self.kwargs['shop_pk'])
        review = get_object_or_404(ShopReview, pk=self.kwargs['pk'])

        form = VoteForm(review, request.user, request.POST)
        if form.is_valid():
            if form.is_up_vote:
                review.vote_up(request.user)
            elif form.is_down_vote:
                review.vote_down(request.user)
            messages.success(request, _("Thanks for voting!"))
        else:
            for error_list in form.errors.values():
                for msg in error_list:
                    messages.error(request, msg)
        return redirect_to_referrer(request, shop.get_absolute_url())


class ShopReviewList(ListView):
    """
    Browse reviews for a Shop
    """
    template_name = 'partner/shopreviews/review_list.html'
    context_object_name = "reviews"
    model = ShopReview
    shop_model = Shop
    paginate_by = settings.OSCAR_REVIEWS_PER_PAGE

    def get_queryset(self):
        qs = self.model.approved.filter(shop=self.kwargs['shop_pk'])
        self.form = SortReviewsForm(self.request.GET)
        if self.form.is_valid():
            sort_by = self.form.cleaned_data['sort_by']
            if sort_by == SortReviewsForm.SORT_BY_RECENCY:
                return qs.order_by('-date_created')
        return qs.order_by('-score')

    def get_context_data(self, **kwargs):
        context = super(ShopReviewList, self).get_context_data(**kwargs)
        context['shop'] = get_object_or_404(
            self.shop_model, pk=self.kwargs['shop_pk'])
        context['form'] = self.form
        return context
