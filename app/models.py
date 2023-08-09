from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.core.validators import RegexValidator
# Create your models here.

STATE_CHOICES = (
    ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
    ("Andhra Pradesh","Andhra Pradesh"),
    ("Arunachal Pradesh	","Arunachal Pradesh"),
    ("Assam","Assam"),
    ("Bihar	","Bihar"),
    ("Chhattisgarh","Chhattisgarh"),
    ("Chandigarh","Chandigarh"),
    ("Dadra & Nagar Haveli and Daman & Diu","Dadra & Nagar Haveli and Daman & Diu"),
    ("Delhi","Delhi"),
    ("Goa","Goa"),
    ("Gujarat","Gujarat"),
    ("Haryana","Haryana"),
    ("Himachal Pradesh	","Himachal Pradesh	"),
    ("Jammu and Kashmir	","Jammu and Kashmir"),
    ("Jharkhand","Jharkhand"),
    ("Karnataka","Karnataka"),
    ("Kerala","Kerala"),
    ("Ladakh","Ladakh"),
    ("Lakshadweep","Lakshadweep"),
    ("Madhya Pradesh","Madhya Pradesh"),
    ("Maharashtra","Maharashtra"),
    ("Manipur","Manipur"),
    ("Meghalaya","Meghalaya"),
    ("Mizoram","Mizoram"),
    ("Nagaland","Nagaland"),
    ("Odisha","Odisha"),
    ("Puducherry","Puducherry"),
    ("Punjab","Punjab"),
    ("Rajasthan","Rajasthan"),
    ("Sikkim","Sikkim"),
    ("Tamil Nadu","Tamil Nadu"),
    ("Telangana","Telangana"),
    ("Tripura","Tripura"),
    ("Uttar Pradesh	","Uttar Pradesh"),
    ("Uttarakhand","Uttarakhand"),
    ("West Bengal","West Bengal	"),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.IntegerField()
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)
    

CATEGORY_CHOICES = (
    ("MB","men-blazers"),
    ("MST","men-shirts"),
    ("MP","men-pants"),
    ("MS","men-shoes"),
    ("MH","men-hats"),
    ("MEW","men-eye-wears"),

    ("TW","top-wear"),
    ("BW","bottom-wear"),
    ("C","Chudidar"),

    ("WS","women-shoes"),
    ("J","jewellery"),
    ("S","saree"),

    ("B","boy"),
    ("G","girl"),


    ("D","designer"),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=4)
    product_image = models.ImageField(upload_to="productimg")

    def __str__(self):
        return str(self.id)
    

class BCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
    @property
    def price(self):
        return self.product.discounted_price
    
    @property
    def pro_image(self):
        return self.product.product_image

STATUS_CHOICES = (
    ("Accepted","Accepted"),
    ("Packed","Packed"),
    ("On The Way","On The Way"),
    ("Delivered","Delivered"),
    ("Cancel","Cancel")
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default="Pending")    

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
    @property
    def price(self):
        return self.product.discounted_price
    


import random


DES_CATEGORY_CHOICES = (
    ("MD","men_designers"),
    ("WD","women_designers"), 
)

def generate_random_number():
    return random.randint(10000, 99999)

class Designer(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    # category = models.CharField(choices=CATEGORY_CHOICES,max_length=4)
    designer_code = models.IntegerField(default=generate_random_number, unique=True)
    full_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)

    phone_regex = r'^\+?1?\d{9,10}$'
    phone = models.CharField(max_length=100, null=True, validators=[RegexValidator(
        regex=phone_regex,)])
    
    work_exp = models.IntegerField()
    address = models.TextField(max_length=100, null=True)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    # des_category = models.CharField(choices=DES_CATEGORY_CHOICES,max_length=4)
    designer_image = models.ImageField(upload_to="designerimg")

    def __str__(self):
        return str(self.id)



DESIGNER_STATUS_CHOICES = (
    ("Accepted","Accepted"),
    
    ("Cancel","Cancel")
)


class DesignerPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=DESIGNER_STATUS_CHOICES, default="Pending")  


class DesignerWorks(models.Model):
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE, related_name='works')
    works_img = models.ImageField(upload_to="works_img")
    descriptions = models.TextField(max_length=500)

    def __str__(self):
        return f"Work {self.id} by Designer {self.designer_id}"



class TempDesignerPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    designer = models.ForeignKey(Designer, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
    verify = models.BooleanField(default=False)