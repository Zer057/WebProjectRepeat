from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from .models import User, Product, Order, OrderItem, ReturnRequest

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (('Role', {'fields': ('role',)}),)
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'created_at')
    inlines = [OrderItemInline]


@admin.register(ReturnRequest)
class ReturnRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_item', 'status', 'created_at', 'processed_by', 'processed_at')
    actions = ['approve_returns', 'reject_returns']

    def approve_returns(self, request, queryset):
        for r in queryset:
            r.status = 'APPROVED'
            r.processed_by = request.user
            r.processed_at = timezone.now()
            r.save()
            # update order status (simple logic)
            order = r.order_item.order
            order.status = 'REFUNDED'
            order.save()
    approve_returns.short_description = "Approve selected return requests"

    def reject_returns(self, request, queryset):
        for r in queryset:
            r.status = 'REJECTED'
            r.processed_by = request.user
            r.processed_at = timezone.now()
            r.save()
    reject_returns.short_description = "Reject selected return requests"
