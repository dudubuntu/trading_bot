from sqlalchemy.types import TypeDecorator
from sqlalchemy import Table, MetaData, Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func as sa_func


class Choices(TypeDecorator):
    impl = String

    cache_ok = True

    def __init__(self, choices):
        self.choices = tuple(choices)
        self.internal_only = True


Base = declarative_base()
meta = MetaData()


class Post(Base):
    __tablename__ = 'admin_proj_post'

    key = Column('key', String(20), primary_key=True)
    message = Column('message', String(5000))
    is_draft = Column('is_draft', Boolean())


class TgUser(Base):
    __tablename__ = 'admin_proj_tguser'
    
    chat_id = Column('chat_id', Integer(), primary_key=True)
    username = Column('username', String(150))
    extra = Column('extra', JSON())
    description = Column('description', String(1000), nullable=True)

    subscription = relationship('Subscription', back_populates='user')


class Rate(Base):
    __tablename__ = 'admin_proj_rate'
    
    month = Column('month', Integer(), primary_key=True)
    description = Column('description', String(500), nullable=True)
    
    subscription = relationship('Subscription', back_populates='rate')


class Subscription(Base):
    __tablename__ = 'admin_proj_subscription'

    id = Column('id', Integer(), primary_key=True)
    rate_id = Column('rate_id', ForeignKey('admin_proj_rate.month'))
    created = Column('created', DateTime(timezone=True), nullable=True)
    is_active = Column('is_active', Boolean())
    user_id = Column('user_id', ForeignKey('admin_proj_tguser.chat_id'))

    user = relationship('TgUser', back_populates='subscription')
    rate = relationship('Rate', back_populates='subscription')


class PaymentSystem(Base):
    __tablename__ = 'admin_proj_paymentsystem'

    slug = Column('slug', String(50), primary_key=True)
    description = Column('description', String(500), nullable=True)
    message = Column('message', String(1000), nullable=True)


class Invoice(Base):
    __tablename__ = 'admin_proj_invoice'

    type_choices = {
        1, "Подписка",
        2, "Обучение",
    }

    id = Column('id', Integer(), primary_key=True)
    user = Column('admin_proj_tguser', ForeignKey('admin_proj_tguser.chat_id'))
    type = Column('type', Choices(type_choices))
    rate = Column('admin_proj_rate', ForeignKey('admin_proj_rate.month'))
    payment_system = Column('admin_proj_payment_system', ForeignKey('admin_proj_payment_system.slug'))
    subscription = Column('admin_proj_subscription', ForeignKey('admin_proj_subscription.id'))
    is_payed = Column('is_payed', Boolean())
    created_at = Column('created_at', DateTime(timezone=True))
    updated_at = Column('updated_at', DateTime(timezone=True), nullable=True)