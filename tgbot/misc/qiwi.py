import uuid
import datetime


async def create_payment(amount: int, obj):
    wallet = obj.bot.get('wallet')
    comment = str(uuid.uuid4())
    waiting_time = datetime.datetime.now() + datetime.timedelta(minutes=10, seconds=20)
    payment = await wallet.create_p2p_bill(
        amount=amount, comment=comment
    )
    return payment


async def check_payment(payment, obj):
    wallet = obj.bot.get('wallet')
    return await wallet.check_p2p_bill_status(bill_id=payment)
