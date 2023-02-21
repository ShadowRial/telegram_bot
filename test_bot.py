@dp.message_handler(lambda message: 'Показать все баки' in message.text)
async def all_buckets(message: types.Message):
    with open('address.json') as file:
        address = json.load(file)

    for k, v in enumerate(address):
        await message.answer(f'Номер: {k + 1} Адрес: {address.get(str(k+1))}')