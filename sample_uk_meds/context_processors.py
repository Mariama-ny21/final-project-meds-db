# sample_uk_meds/context_processors.py

def cart_count(request):
    cart = request.session.get('cart', {})
    def get_qty(item):
        if isinstance(item, dict):
            return item.get('quantity', 0)
        try:
            return int(item)
        except Exception:
            return 0
    count = sum(get_qty(item) for item in cart.values())
    return {'cart_count': count}
