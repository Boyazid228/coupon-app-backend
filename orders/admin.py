from django.contrib import admin
from . import models


@admin.register(models.Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'product_name', 'payment', 'status', 'created_at', 'updated_at')
    list_filter = ('product', 'created_at', 'updated_at', 'status', 'payment')
    search_fields = ('product__name', 'user__username', 'status', 'payment')

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status":
            choices = list(db_field.choices)
            choices = [("accepted", "Accepted"), ("denied", "Denied")]
            if request.user.is_superuser:
                choices.append(("ready", "Payed"))
            kwargs["choices"] = choices
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    @admin.display(ordering='product__name', description="Product Name")
    def product_name(self, instance):
        return instance.product.name if instance.product else "No Product"

    @admin.display(ordering='user__username', description="User Name")
    def user_username(self, instance):
        return instance.user.username if instance.user else "No User"
