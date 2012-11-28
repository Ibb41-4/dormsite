from datetime import date, datetime
from decimal import Decimal

from django.db import models
from django.db.models.signals import post_init
from django.conf import settings 


from core.models import TrackableModel
from user_details.models import User


class Balance(TrackableModel):
    preview = models.BooleanField(editable=False)

    @classmethod
    def get_latest(cls):
        try: 
            return cls.objects.filter(preview=False).latest('created')
        except cls.DoesNotExist:
            return cls(created=datetime.now())   

    @property
    def previous(self):
        if not self.pk:
            return None

        try:
            return self.get_previous_by_created(preview=False)
        except self.model.DoesNotExist:
            return self.model(created=datetime.now())

    @property
    def next(self):
        if not self.pk:
            return None

        try: 
            return self.get_next_by_created()
        except self.model.DoesNotExist:
            return None

    @classmethod
    def update_preview(cls, sender, instance, **kwargs):
        if cls != Balance or not instance.preview or not instance.pk:
            return

        previous_balance = instance.previous
        
        new_balance = instance
        new_balance.created = datetime.now()

        #get all data since last balance
        dinners = Dinner.objects.filter(created__gt=previous_balance.created)
        expenses = Expense.objects.filter(created__gt=previous_balance.created)
        drinks = Drink.objects.filter(created__gt=previous_balance.created)
        bills = Bill.objects.filter(created__gt=previous_balance.created)

        for user in User.objects.all():

            #get previous total (0 if none exists)
            try:
                previous_total = previous_balance.rows.get(user=user).total
            except BalanceRow.DoesNotExist:
                previous_total = 0

            #skip user which don't live here yet or not anymore and have a total of zero
            today = date.today()
            if not user.startdate or (user.startdate > today
                or  ( user.enddate 
                    and user.enddate < previous_balance.created 
                    and previous_total == 0 )):
                continue

            #get sums of data for this user
            sum_expenses =      sum(map(lambda x: x.price, expenses.filter(payer=user)))
            sum_dinners_payed = sum(map(lambda x: x.price, dinners.filter(payer=user)))
            sum_payed =         sum(map(lambda x: x.price, bills.filter(payer=user)))
            sum_drinks =        sum(map(lambda x: x.price * x.number, drinks.filter(payer=user)))

            def consumed_price(dinner, user):
                number_of_eaters = sum(map(lambda x: 1 + x.extra, dinner.eater_set.all()))
                indiviual_price = dinner.price / number_of_eaters
                user_price = indiviual_price * (dinner.eater_set.get(user=user).extra+1)
                return user_price

            sum_dinners_eaten = sum(map(lambda dinner: consumed_price(dinner, user), dinners.filter(eaters=user)))



            #calculate monthly fee using proper start and end dates
            startdate = max(previous_balance.created.date(), user.startdate)
            enddate = min(date.today(), user.enddate) if user.enddate else date.today()
            monthly_fee = Decimal(settings.MONTHLY_FEE * number_months(startdate, enddate))
         
            #calculate totals
            total_credit = sum_drinks + sum_dinners_eaten + monthly_fee
            total_debit = sum_expenses + sum_dinners_payed + sum_payed
           
            total = previous_total - total_debit + total_credit

            balance_row, was_created = BalanceRow.objects.get_or_create( 
                user = user, 
                balance = new_balance,
                defaults = {
                    'last_balance': previous_total, 
                    'payed': sum_payed,
                    'monthly_fee': monthly_fee,
                    'expenses': sum_expenses,
                    'dinners': sum_dinners_eaten - sum_dinners_payed,
                    'drinks': sum_drinks,
                    'total': total
                }
            )
            balance_row.last_balance = previous_total
            balance_row.payed = sum_payed
            balance_row.monthly_fee = monthly_fee
            balance_row.expenses = sum_expenses
            balance_row.dinners = sum_dinners_eaten - sum_dinners_payed
            balance_row.drinks = sum_drinks
            balance_row.total = total
            balance_row.save()
    class Meta:
        permissions = (
            ("view_balance", "Can see balances"),
        )

def number_months(startdate, enddate):
    """
    Get the number of months between two dates
    """
    return (enddate.year-startdate.year)*12 + (enddate.month - startdate.month)


post_init.connect(Balance.update_preview, Balance)

class BalanceRow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    balance = models.ForeignKey(Balance, related_name="rows")
    last_balance = models.DecimalField(max_digits=7, decimal_places=2)
    payed = models.DecimalField(max_digits=7, decimal_places=2)
    expenses = models.DecimalField(max_digits=7, decimal_places=2)
    monthly_fee = models.DecimalField(max_digits=7, decimal_places=2)
    dinners = models.DecimalField(max_digits=7, decimal_places=2)
    drinks = models.DecimalField(max_digits=7, decimal_places=2)
    total = models.DecimalField(max_digits=7, decimal_places=2)

class PaymentModel(TrackableModel):
    payer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="payed_%(class)ss")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        abstract = True

class DescriptionPaymentModel(PaymentModel):
    description = models.TextField()

    def __unicode__(self):
        description = (self.description[:75] + '..') if len(self.description) > 75 else self.description
        return u"\u20ac %s voor %s" % (self.price, description)

    class Meta:
        abstract = True

class Bill(DescriptionPaymentModel):
    pass

class Expense(DescriptionPaymentModel):
    pass

class Drink(PaymentModel):
    number = models.PositiveIntegerField()

    def __unicode__(self):
        return u"%s eenheden a %s door %s" % (self.number, self.price, self.user)

class Dinner(PaymentModel):
    eaters = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="%(class)ss", through='Eater')
    
    def __unicode__(self):
        return u"Eten voor %s" % self.price

class Eater(models.Model):
    dinner = models.ForeignKey(Dinner)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    extra = models.PositiveIntegerField()
