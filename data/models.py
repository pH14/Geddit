from django.db import models
import smtplib
from email.mime.text import MIMEText
from googlevoice import Voice

USERNAME_MAX_LENGTH = 25
PERSON_NAME_MAX_LENGTH = 25
PHONE_NUMBER_MAX_LENGTH = 20

GEDDIT_GMAIL = 'awib5dche9di@gmail.com'
GEDDIT_PASSWORD = '' # You should fill this in

class User(models.Model):
    # The id field is automatically generated by Django
    # id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=USERNAME_MAX_LENGTH, unique=True)
    first_name = models.CharField(max_length=PERSON_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=PERSON_NAME_MAX_LENGTH)
    email = models.EmailField()
    cell_phone = models.CharField(max_length=PHONE_NUMBER_MAX_LENGTH)

    def __unicode__(self):
        return self.last_name + ', ' + self.first_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @staticmethod
    def create_user(username, first_name, last_name, email, cell_phone):
        u = User(username=username, first_name=first_name, \
                last_name=last_name, email=email, cell_phone=cell_phone)
        u.save()
        return u

    @staticmethod
    def get_user(username):
        return User.objects.get(username=username)

    @staticmethod
    def delete_user(user):
        user.delete()

    def send_email(self, message, subject):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = GEDDIT_GMAIL
        msg['To'] = self.email

        s = smtplib.SMTP('localhost')
        s.sendmail(GEDDIT_GMAIL, [self.email], msg.as_string())
        s.quit()

    def send_sms(self, message):
        voice = Voice()
        voice.login(GEDDIT_GMAIL, GEDDIT_PASSWORD)
        voice.send_sms(self.cell_phone, message)

    def add_item(self, name, description, category):
        return Item.create_item(self, name, description, category)

    def get_items(self):
        return Item.get_items(self)

    def add_claim(self, item):
        return Claim.create_claim(self, item)

    def get_claims(self):
        return Claim.get_claims(self)

CATEGORY_NAME_MAX_LENGTH = 100

class Category(models.Model):
    # Django will automatically generate this:
    # id = models.IntegerField()
    name = models.CharField(max_length=CATEGORY_NAME_MAX_LENGTH)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    @staticmethod
    def create_category(name):
        c = Category(name=name)
        c.save()
        return c

    @staticmethod
    def get_category(name):
        return Category.objects.get(name=name)

    @staticmethod
    def delete_category(category):
        category.delete()

ITEM_NAME_MAX_LENGTH = 100
DESCRIPTION_NAME_MAX_LENGTH = 1000

class Item(models.Model):
    # Django will automatically generate this:
    # id = models.IntegerField()
    seller_user = models.ForeignKey(User)
    name = models.CharField(max_length=ITEM_NAME_MAX_LENGTH)
    description = models.CharField(max_length=DESCRIPTION_NAME_MAX_LENGTH)
    active = models.BooleanField()
    category = models.ForeignKey(Category)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    @staticmethod
    def create_item(seller_user, name, description, category):
        i = Item(seller_user=seller_user, name=name, description=description, \
                active=True, category=category)
        i.save()
        return i

    @staticmethod
    def get_items(seller_user):
        return Item.objects.filter(seller_user=seller_user)

    @staticmethod
    def delete_item(item):
        item.delete()

class Filter(models.Model):
    # Django will automatically generate this:
    # id = models.IntegerField()
    user = models.ForeignKey(User)
    conditions = models.CharField(max_length=DESCRIPTION_NAME_MAX_LENGTH)
    timestamp = models.TimeField()

    def __unicode__(self):
        return self.conditions

    class Meta:
        verbose_name = 'Filter'
        verbose_name_plural = 'Filters'

class Claim(models.Model):
    # Django will automatically generate this:
    # id = models.IntegerField()
    buyer = models.ForeignKey(User, related_name='buyer')
    item = models.ForeignKey(Item)

    def __unicode__(self):
        return str(self.buyer) + ' ' + str(item)

    class Meta:
        verbose_name = 'Claim'
        verbose_name_plural = 'Claims'

    @staticmethod
    def create_claim(buyer, item):
        c = Claim(buyer=buyer, item=item)
        c.save()
        return c

    @staticmethod
    def get_claims(buyer):
        return Claim.objects.filter(buyer=buyer)

    @staticmethod
    def delete_claim(claim):
        claim.delete()
