import datetime
from django.db import models
from django.utils import timezone


class Post(models.Model):
    key = models.CharField('Ключ поста', primary_key=True, max_length=20)
    message = models.TextField('Сообщение', max_length=5000)
    is_draft = models.BooleanField('Черновик', default=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class TgUser(models.Model):
    chat_id = models.PositiveIntegerField(verbose_name="Telegram Chat id", primary_key=True)
    username = models.CharField(max_length=150, verbose_name='Псевдоним', unique=True)
    extra = models.JSONField(blank=True, null=True)
    description = models.CharField('Дополнительное описание', blank=True, null=True, max_length=1000)

    class Meta:
        verbose_name = "Пользователь tg"
        verbose_name_plural = "Пользователи tg"

    @property
    def has_active_subscription(self):
        if hasattr(self, "subscription"):
            if self.subscription.is_active:
                return True
        return False


class Rate(models.Model):
    month = models.PositiveSmallIntegerField('Длительность подписки мес', primary_key=True)
    description = models.CharField(max_length=500, blank=True, null=True)


class Subscription(models.Model):
    user = models.OneToOneField(TgUser, on_delete=models.CASCADE, to_field="chat_id", related_name="subscription")
    rate = models.ForeignKey(Rate, on_delete=models.DO_NOTHING, to_field="month")
    created = models.DateTimeField("Дата начала подписки", auto_now=True)
    is_active = models.BooleanField("Подписка активна", default=False)

    @property
    def end_at(self) -> datetime.datetime:
        return self.created + datetime.timedelta(weeks=self.rate.month * 4)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class PaymentSystem(models.Model):
    #TODO добавить поле keyboard_name и генерацию клавиатуры в trading_bot
    slug = models.SlugField("Уникальный slug", primary_key=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    message = models.TextField(verbose_name='Сообщение пользователю при оплате', max_length=1000)
    
    class Meta:
        verbose_name = "Платежная система"
        verbose_name_plural = "Платежные системы"


class Invoice(models.Model):
    type_list = (
        (1, "Подписка"),
        (2, "Обучение")
    )

    user = models.ForeignKey(TgUser, on_delete=models.DO_NOTHING, to_field="chat_id", related_name='invoice_list')
    type = models.PositiveSmallIntegerField("Тип оплаты", choices=type_list)
    rate = models.ForeignKey(Rate, on_delete=models.DO_NOTHING, to_field="month", null=True)
    payment_system = models.ForeignKey(PaymentSystem, on_delete=models.DO_NOTHING, to_field='slug')
    subscription = models.ForeignKey(Subscription, on_delete=models.DO_NOTHING, null=True, related_name="invoice_list")
    is_payed = models.BooleanField("Инвойс оплачен", default=False)
    created_at = models.DateTimeField("Дата создания", auto_now=True)
    updated_at = models.DateTimeField("Дата оплаты", null=True)

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Инвойс"
        verbose_name_plural = "Инвойсы"