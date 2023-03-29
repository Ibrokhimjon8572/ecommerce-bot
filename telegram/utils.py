from functools import lru_cache
from django.utils.translation import gettext as _
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="ecommerce-bot")


def number_to_emoji(number):
    emojies = {
        '0': "0️⃣",
        '1': "1️⃣",
        '2': "2️⃣",
        '3': "3️⃣",
        '4': "4️⃣",
        '5': "5️⃣",
        '6': "6️⃣",
        '7': "7️⃣",
        '8': "8️⃣",
        '9': "9️⃣",
    }
    res = [emojies[i] for i in str(number)]
    return "".join(res)


def format_number(number):
    return f"{number:,}".replace(",", " ")


def generate_text(items, lang):
    text = ""
    price = 0
    for item in items:
        name = item.product.name_uz if lang == 'uz' else item.product.name_ru
        text += _("%(name)s ✖️ %(amount)s: %(price)s\n") % {
            "name": name, "amount": number_to_emoji(item.amount), "price": format_number(item.price * item.amount)}
        price += item.price * item.amount
    text += "\n\n"
    text += _("total: %(price)s so'm") % {"price": format_number(price)}
    return text


@lru_cache
def get_address(lat, long):
    try:
        location = geolocator.reverse((lat, long))
        print(location, dir(location))
        return str(location)
    except:
        return ""
