from django import forms
from product.models import *
from banner.models import *
from coupon.models import *
from rating.models import *
from checkout.models import *
# from seo_settings.m/odels import *
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.widgets import FilteredSelectMultiple

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from product.models import *
User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter User Name here...'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email here...'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields.pop('password1')  # Remove password field from the form
    #     self.fields.pop('password2')  # Remove password confirmation field from the form

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            # Generate a random password
            password = get_random_string(length=12)

            # Set the random password for the user
            user.set_password(password)
            user.save()

            # Send the email to the user
            subject = 'Your account has been created'
            reset_password_url =f'https://suwaidionline.com/forgot_password'
            message = f'Your username: {user.email}\nYour password: {password}\nReset password link: {reset_password_url}'
            from_email = 'onlineorders@suwaidillc.ae'  # Update with your email
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])
        return user
    


class CsvImportForm(forms.Form):
    csv_upload = forms.FileField()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = ParentCategory
        # fields = '__all__'
        fields = ['name', 'image', 'slot_position','active']


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        # fields = '__all__'
        # fields = ['main_Category','name', 'image', 'Active', 'Slot_Position']
        fields = ['parent_category','name', 'image', 'slot_position','active']



class ChildSubCategoryForm(forms.ModelForm):
    class Meta:
        model = ChildSubCategory
        # fields = '__all__'
        fields = ['sub_category','name', 'image', 'slot_position','active']


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


# class CouponForm(forms.ModelForm):
#     class Meta:
#         model = Coupon
#         fields = ['code', 'discount', 'valid_from', 'valid_to', 'active']


# class RatingsForm(forms.ModelForm):
#     class Meta:
#         model = Rating
#         fields = [ 'user','review ', 'review_date', 'anonymous', 'active']










# class CouponForm(forms.ModelForm):
#     class Meta:
#         model = Coupon
#         fields = ['code', 'discount', 'valid_from', 'valid_to', 'Active']


# class mainbanner Form(forms.ModelForm):
#     class Meta:
#         model = mainbanner 
#         fields = ['banner', 'banner_url', 'Slot_Position', 'Active']


# class OfferBannerForm(forms.ModelForm):
#     class Meta:
#         model = offer_banner
#         fields = '__all__'  # You can specify the fields explicitly if needed


# BANNER 

class mainBannerForm(forms.ModelForm):
    class Meta:
        model = MainBanner
        # fields = ['banner', 'banner_head', 'banner_para', 'categories', 'Slot_Position', 'Active']
        fields = ['banner_image','alt_text','url','slot_position','active']


# class TrendingBannerForm(forms.ModelForm):
#     class Meta:
#         model = TrendingBrand
#         fields = ['brand ', 'url ','alt_text','Slot_Position', 'active ']

class PriceBannerForm(forms.ModelForm):
    Category = forms.ModelChoiceField(
        queryset=ParentCategory.objects.all(),
        required=False,
        label="Parent Category"
        )
    class Meta:
        model = PriceBanner
        # Category=ParentCategory.name

        fields = ['Category','alt_text','image','slot_position' ,'active']

class FooterBannerForm(forms.ModelForm):
    class Meta:
        model = FooterBanner
        fields = ['banner_image','alt_text','slot_position','active']


# # forms.py
# from django import forms
# from .models import Category

# class CategoryForm(forms.Form):
#     parent_category = forms.ModelChoiceField(queryset=Category.objects.filter(parent__isnull=True), required=False)
#     child_category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False)

#     def __init__(self, *args, **kwargs):
#         parent_category_id = kwargs.pop('parent_category_id', None)
#         super(CategoryForm, self).__init__(*args, **kwargs)
        
#         if parent_category_id:
#             self.fields['child_category'].queryset = Category.objects.filter(parent_id=parent_category_id)
#         else:
#             self.fields['child_category'].queryset = Category.objects.none()






class TagsForms(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'description']


# class CategoryBannerForm(forms.ModelForm):
#     Category = forms.ModelChoiceField(
#         queryset=Category.objects.all(),
#         widget=forms.Select(
#             attrs={
#                 'class': 'form-select',
#                 'data-placeholder': 'Select Category',
#                 'id': 'categorySelect',  # Update ID if necessary
#                 'data-choices': 'data-choices',
#                 'data-options': '{"removeItemButton":true,"placeholder":true}'
#             }
#         ),
#         label='Category'
#     )

#     class Meta:
#         model = categorybanner
#         fields = ['Category', 'banner', 'Slot_Position', 'Active']

















class GroupCreationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write Name here...'})
    )

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'organizerMultiple', 'multiple': 'multiple', 'data-choices': 'data-choices', 'data-options': '{"removeItemButton":true,"placeholder":true}'})
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']






class GroupChangeForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write Name here...'})
    )

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'organizerMultiple', 'multiple': 'multiple', 'data-choices': 'data-choices', 'data-options': '{"removeItemButton":true,"placeholder":true}'})
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class OrderDeliveryPersonForm(forms.ModelForm):

    delivery_person_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write Name here...'})
    )

    contact = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write Name here...'})
    )

    order = forms.ModelChoiceField(
        queryset=Order.objects.all(),  
        widget=forms.Select(attrs={'class': 'form-select updated-class', 'id': 'organizerSingle', 'data-choices': 'data-choices', 'data-options': '{"removeItemButton":true,"placeholder":true}'}),
        empty_label="Select an order"  # Optional: Add an empty label to display as the default option
    )
    
    # class Meta:
    #     model = OrderDeliveryPerson
    #     fields = ['order', 'delivery_person_name', 'contact']

    def clean_order(self):
        order_instance = self.cleaned_data.get('order')
        if not order_instance:
            raise forms.ValidationError("Please select an order")
        return order_instance



class ReplacementCollectPersonForm(forms.ModelForm):

    collect_person_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write Name here...'})
    )

    contact = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write Name here...'})
    )

    collect_Date = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control datetimepicker flatpickr-input', 'id': 'datepicker', 'placeholder': 'yyyy/mm/dd', 'readonly': 'readonly', 'data-options':'{"&quot;disableMobile&quot;:true,&quot;dateFormat&quot;:&quot;Y-m-d&quot;}"}'})
    )

    order = forms.ModelChoiceField(
        queryset=Order.objects.all(),  
        widget=forms.Select(attrs={'class': 'form-select updated-class', 'id': 'organizerSingle', 'data-choices': 'data-choices', 'data-options': '{"removeItemButton":true,"placeholder":true}'}),
        empty_label="Select an order"  # Optional: Add an empty label to display as the default option
    )

    # class Meta:
    #     model = ReplacementCollectPerson
    #     fields = ['order', 'collect_person_name', 'contact', 'collect_Date']
        # widgets = {
        #     'order': forms.Select(attrs={'class': 'form-select'}),
        #     'collect_person_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'contact': forms.TextInput(attrs={'class': 'form-control'}),
        #     'collect_Date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        # }


    def clean_order(self):
        order_instance = self.cleaned_data.get('order')
        if not order_instance:
            raise forms.ValidationError("Please select an order")
        return order_instance




class UserPermissionForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'data-placeholder': 'Select User', 'id': 'organizerSingle', 'data-choices': 'data-choices', 'data-options': '{"removeItemButton":true,"placeholder":true}'}),
        label='User'
    )
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'organizerMultipleUser', 'multiple': 'multiple', 'data-choices': 'data-choices', 'data-options': '{"removeItemButton":true,"placeholder":true}'}),
        label='User Permissions',
        required=False  # Make this field optional
    )
    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'organizerMultipleGroup', 'multiple': 'multiple', 'data-choices': 'data-choices', 'data-options': '{"removeItemButton":true,"placeholder":true}'}),
        label='Group Permissions',
        required=False  # Make this field optional
    )

    class Meta:
        model = User
        fields = ['user', 'permissions', 'group']


class UserPermissionChangeForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'organizerMultiple', 'multiple': 'multiple', 'data-choices': 'data-choices', 'data-options': '{"removeItemButton":true,"placeholder":true}'}),
        label='User Permissions',
        required=False  # Make this field optional
    )

    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'organizerMultipleGroup', 'multiple': 'multiple', 'data-choices': 'data-choices', 'data-options': '{"removeItemButton":true,"placeholder":true}'}),
        label='Group Permissions',
        required=False  # Make this field optional
    )

    class Meta:
        model = User
        fields = ['permissions', 'group']

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super(UserPermissionChangeForm, self).__init__(*args, **kwargs)
        if user_instance:
            self.fields['permissions'].queryset = user_instance.user_permissions.all()

            # Set initial value for the group field if user_instance has groups
            if user_instance.groups.exists():
                self.fields['group'].initial = user_instance.groups.all()



# class RobotsTxtForm(forms.ModelForm):
#     class Meta:
#         model = RobotsTxt
#         fields = ['content']

# class GoogleTagManagerForm(forms.ModelForm):
#     position = forms.ChoiceField(choices=GoogleTagManager.SCRIPT_CHOICES, widget=forms.Select(attrs={'class': 'form-select', 'data-choices': 'data-choices', 'data-options': '{"removeItemButton":true,"placeholder":true}'}))
#     class Meta:
#         model = GoogleTagManager
#         fields = ['script_name', 'script_code', 'position']


class OfferForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),  # Assuming you have a Product model
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Product'
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write Name here...'}),
        label='Name'
    )
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker flatpickr-input',
            'placeholder': 'dd/mm/yyyy hour : minute',
            'data-options': '{"enableTime":true,"dateFormat":"d/m/Y H:i","disableMobile":true}'
        }),
        label='Start Date',
        input_formats=['%d/%m/%Y %H:%M']
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker flatpickr-input',
            'placeholder': 'dd/mm/yyyy hour : minute',
            'data-options': '{"enableTime":true,"dateFormat":"d/m/Y H:i","disableMobile":true}'
        }),
        label='End Date',
        input_formats=['%d/%m/%Y %H:%M']
    )
    badge_value = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Badge Value'}),
        label='Badge Value'
    )

    # class Meta:
    #     model = Offer
    #     fields = ['product', 'name', 'start_date', 'end_date', 'badge_value']






























# class CustomSelectMultiple(forms.SelectMultiple):
#     def __init__(self, attrs=None):
#         default_attrs = {'class': 'form-select', 'id': 'organizerMultiple', 'multiple': 'multiple', 'data-choices': 'data-choices', 'data-options': '{"removeItemButton":true,"placeholder":true}'}
#         if attrs:
#             default_attrs.update(attrs)
#         super().__init__(attrs=default_attrs)

# class GroupCreationForm(forms.ModelForm):
#     permissions = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.all(),
#         widget=CustomSelectMultiple()
#     )

#     class Meta:
#         model = Group
#         fields = ['name', 'permissions']
        
