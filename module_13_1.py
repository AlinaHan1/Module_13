import asyncio


async def start_strongman(name, power):  # Для обозначения асинхронной функции используйте оператор async
    print(f'Силач {name} начал соревнование')
    for i in range(5):
        await asyncio.sleep(1 / power)  # Для задержки в асинхронной функции используйте функцию sleep из пакета asyncio
        print(f'Силач {name} поднял {i + 1}')
    print(f'Силач {name} закончил соревнование')


async def start_tournament():
    task_1 = asyncio.create_task(start_strongman('Pasha', 3))
    task_2 = asyncio.create_task(start_strongman('Denis', 4))
    task_3 = asyncio.create_task(start_strongman('Apollon', 5))
    await task_1  # Для постановки задачи в режим ожидания используйте оператор await
    await task_2
    await task_3


asyncio.run(start_tournament())  # Для запуска асинхронной функции используйте функцию run из пакета asyncio
