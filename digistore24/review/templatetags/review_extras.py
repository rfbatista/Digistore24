from django import template

register = template.Library()


@register.filter
def get_decision_display(value):
    mapping = {
        1: "Confirm ✅",
        2: "Override ❌",
    }
    return mapping.get(value, value)
