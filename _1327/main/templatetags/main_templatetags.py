from django.template import Library

register = Library()


@register.inclusion_tag("menu_items_list.html")
def include_menu_items_list(items, user):
	return dict(items=items, user=user)
