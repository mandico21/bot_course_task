from io import BytesIO

import aiohttp
from aiogram import Bot
from aiogram.types import photo_size


async def photo_url(photo: photo_size.PhotoSize) -> str:
    bot = Bot.get_current()
    with await photo.download(destination_file=BytesIO()) as file:
        form = aiohttp.FormData()
        form.add_field(
            name='file',
            value=file,
        )
        async with bot.session.post('https://telegra.ph/upload', data=form) as response:
            img_src = await response.json()

    return 'https://telegra.ph/' + img_src[0]["src"]
