from tax import calculate_tax


def checkout(amount):
    return amount + calculate_tax(amount)