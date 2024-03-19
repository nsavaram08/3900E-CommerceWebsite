from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Item, Category, Order, OrderItem, SubCategory
from django.urls import reverse
from django import forms
import csv
import datetime
from django.http import HttpResponse



def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('Nile:admin_order_detail', args=[obj.id])))


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' \
                                      'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('Nile:admin_order_pdf', args=[obj.id])))


order_pdf.short_description = 'Invoice'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_detail, order_pdf]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]


class SubCategoryAdminForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = '__all__'

class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryAdminForm
    list_display = ['id', 'name']

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(SubCategory, SubCategoryAdmin)



