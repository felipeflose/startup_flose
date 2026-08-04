def calculate_total(items):
    total = sum(item['price'] * item['quantity'] for item in items)
    return total