from datetime import date
from django.shortcuts import render, get_object_or_404
from .models import Promotion, ProductsOnPromotion

def promotion_list(request):
    promotions = Promotion.objects.all()
    return render(request, 'promotions/promotion_list.html', {'promotions': promotions})

def promotion_detail(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    products_on_promotion = ProductsOnPromotion.objects.filter(promotion_id=promotion)

    # Check if the promotion end date has passed
    if promotion.promo_end < date.today():
        # Deactivate products associated with the promotion
        products_on_promotion.update(is_active=False)

    return render(request, 'promotions/promotion_detail.html', {'promotion': promotion, 'products_on_promotion': products_on_promotion})
