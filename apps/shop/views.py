from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import SessionWizardView

from .forms import ShopBasicInfoForm, ShopBrandingForm, ShopPaymentForm, ShopProductImportForm
from .models import Shop, ShopBranding, ShopPayment, ShopProduct

FORMS = [
    ('basic', ShopBasicInfoForm),
    ('branding', ShopBrandingForm),
    ('payment', ShopPaymentForm),
    ('products', ShopProductImportForm),
    ('review', None),  # No form, just review step
]

TEMPLATES = {
    'basic': 'shop/wizard_basic.html',
    'branding': 'shop/wizard_branding.html',
    'payment': 'shop/wizard_payment.html',
    'products': 'shop/wizard_products.html',
    'review': 'shop/wizard_review.html',
}

class ShopCreateWizard(LoginRequiredMixin, SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # Retrieve forms
        basic_form = self.get_form(step='basic')
        branding_form = self.get_form(step='branding')
        payment_form = self.get_form(step='payment')
        product_form = self.get_form(step='products')

        # Create Shop instance
        shop = basic_form.save(commit=False)
        shop.owner = self.request.user
        shop.save()

        # Branding
        branding = branding_form.save(commit=False)
        branding.shop = shop
        branding.save()

        # Payment
        payment = payment_form.save(commit=False)
        payment.shop = shop
        payment.save()

        # Products (CSV import or manual first product)
        if product_form.cleaned_data.get('csv_file'):
            import csv, io
            file_data = product_form.cleaned_data['csv_file'].read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(file_data))
            for row in reader:
                ShopProduct.objects.create(
                    shop=shop,
                    name=row.get('name'),
                    price=row.get('price'),
                )
        else:
            if product_form.cleaned_data.get('name'):
                ShopProduct.objects.create(
                    shop=shop,
                    name=product_form.cleaned_data['name'],
                    price=product_form.cleaned_data['price'],
                    image=product_form.cleaned_data.get('image'),
                )
        # Redirect to a placeholder detail view (to be implemented later)
        return redirect('shop:detail', pk=shop.pk)
