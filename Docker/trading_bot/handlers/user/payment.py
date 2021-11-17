from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.payment import buy_course_kb, buy_subscription_kb, confirm_pay_kb
from keyboards.default import back_kb
from states.user.payment import *


async def payment_course(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["amount"] = 10000
        data["type"] = "Course"
    await PaymentStates.PaymentInitialized.set()
    await choose_payment(msg, state)

async def payment_subscription(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["type"] = "Subscription"
    await PaymentStates.PaymentInitialized.set()
    await msg.answer(text="Выберите длительность подписки", reply_markup=buy_subscription_kb)

async def choose_payment(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data["type"] == "Subscription":
            data["amount"] = int(msg.text.split("(")[1].strip("р)"))
            data["duration"] = int(msg.text.split(" ")[0].strip())

    await msg.answer(text="Выберите тип оплаты", reply_markup=buy_course_kb)
    await PaymentStates.PaymentChosen.set()

async def payment_confirm(msg: types.Message, state: FSMContext):
    text = "Подтвердите оплату %s:\nСтоимость %sр"
    async with state.proxy() as data:
        if data["type"] == "Course":
            text = text % ("курса", data["amount"])
        elif data["type"] == "Subscription":
            text = text % (f"подписки на {data['duration']} месяца", data["amount"])
            
    await msg.answer(text=text, reply_markup=confirm_pay_kb)
    await PaymentStates.PaymentConfirmed.set()

async def payment_finish(msg: types.Message, state: FSMContext):
    await msg.answer(text="Перейдите по cсылке для оплаты:\nhttps://google.com", reply_markup=back_kb)
    await PaymentStates.PaymentFinished.set()