from django.contrib import admin

from oscar.core.loading import get_model

ShopReview = get_model('shopreviews', 'ShopReview')


class ShopReviewAdmin(admin.ModelAdmin):
    list_display = ('shop', 'title', 'score', 'status', 'total_votes',
                    'delta_votes', 'date_created')
    readonly_fields = ('total_votes', 'delta_votes')


class VoteAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'delta', 'date_created')

admin.site.register(ShopReview, ShopReviewAdmin)
