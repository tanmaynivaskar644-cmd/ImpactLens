from checkout import checkout


def place_order(amount):
    return {
        "subtotal": amount,
        "total": checkout(amount),
    }


if __name__ == "__main__":
    print(place_order(100))