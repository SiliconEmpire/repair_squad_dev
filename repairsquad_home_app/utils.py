import random
import string

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_repair_order_id_generator(instance):
    repair_order_new_id= random_string_generator()

    Klass= instance.__class__

    qs_exists= Klass.objects.filter(order_id = repair_order_new_id).exists()
    if qs_exists:
        return unique_repair_order_id_generator(instance)
    return repair_order_new_id