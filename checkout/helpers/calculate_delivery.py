def calculate_delivery_cost(order):
    """
    Set the delivery cost for the Order based on it being a domestic (IE)
    or international (EU) order.
    Need to call order.save() after calling.
    """
    if order.country.code == "IE":
        order.delivery_cost = 4.50
        order.delivery_method = "An Post"
    else:
        order.delivery_cost = 10.00
        order.delivery_method = "DHL"
