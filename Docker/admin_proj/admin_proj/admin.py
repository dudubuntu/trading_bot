from django.contrib import admin

from .models import *


class InvoiceInline(admin.StackedInline):
    model = Invoice
    fields = ["id", "type", "rate", "is_payed", "created_at", "updated_at"]
    readonly_fields = ['created_at']
    extra = 0


class SubscriptionInline(admin.StackedInline):
    model = Subscription
    fields = ["rate", "is_active", "created"]
    readonly_fields = ['created']
    extra = 0

    @admin.display
    def rate(self, obj):
        return f"{obj.rate} мес"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ["key", "message", "is_draft"]
    list_display = ["key", "post", "is_draft"]
    list_editable = ["is_draft"]
    list_filter = ["is_draft"]
    search_fields = ["key", "post"]
    

    @admin.display
    def post(self, obj):
        return f"{obj.message[:30]}..."


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    # actions = []
    # actions_on_top = True
    fieldsets = (
        (None, {"fields": ["chat_id", "username"]}),
        ("extra", {"fields": ["extra", "description"],
                   "classes": ["collapse"]})
    )
    inlines = [SubscriptionInline, InvoiceInline]
    list_display = ["chat_id", "username", "has_active_subscription"]
    readonly_fields = ["chat_id", "username"]
    # list_filter = ["has_active_subscription"]  нужно дописать логику
    search_fields = ["chat_id", "username", "extra", "description"]

    @admin.display
    def has_active_subscription(self, obj):
        return obj.has_active_subscription


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    # actions = []
    # actions_on_top = True
    # fieldsets = (
    #     (None, {"fields": ("id", "user")}),
    #     (None, {"fields": ("type", "rate"),
    #                "classes": ("collapse", )}),
    #     (None, {"fields": ("is_payed", ("created_at", "updated_at")),
    #                "classes": ("collapse", )}),
    # )
    fields = ["id", "user", "username", "type", "rate", "payment_system", "subscription", "is_payed", "created_at", "updated_at"]
    readonly_fields = ['created_at']
    list_display = ["id", "user", "username", "has_active_subscription"]
    readonly_fields = ["id", "user", "username", "created_at"]
    # list_filter = ["has_active_subscription"]
    search_fields = ["id", "user", "username", "extra", "description"]

    @admin.display
    def has_active_subscription(self, obj):
        return obj.has_active_subscription
    
    @admin.display
    def username(self, obj):
        return obj.user.username


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    fields = ["user", "rate", "created", "is_active"]
    readonly_fields = ["created"]
    list_display = ["user", "rate", "is_active"]


# admin.site.register(Invoice)
admin.site.register(Rate)
admin.site.register(PaymentSystem)