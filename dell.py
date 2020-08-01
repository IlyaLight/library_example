import asyncio
from random import randint


class Rocket:
    def __init__(self):
        self.delay = randint(0, 3)
        self.countdown = randint(1, 5)

    def launch_rocket(self):
        time.sleep(self.delay)
        for i in reversed(range(self.countdown)):
            print(f"{i + 1}...")
            time.sleep(1)
        print("Rocket launched!")

    @staticmethod
    async def async_launch_rocket(q: asyncio.Queue):
        rocket = await q.get()
        await asyncio.sleep(rocket.delay)
        for i in reversed(range(rocket.countdown)):
            print(f"{i + 1}...")
            await asyncio.sleep(1)
        print("Rocket launched!")
        q.task_done()


class Spaceport:
    def __init__(self, number_of_launch_sites=10):
        self.number_of_launch_sites = number_of_launch_sites

    async def _async_launch(self, rockets):
        rocket_queue = asyncio.Queue()
        for rocket in rockets:
            rocket_queue.put_nowait(rocket)

        tasks = []
        for i in range(self.number_of_launch_sites):
            task = asyncio.create_task(Rocket.async_launch_rocket(rocket_queue))
            tasks.append(task)

        await rocket_queue.join()
        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

    async def launch_rockets(self, q: asyncio.Queue):
        while True:
            rockets = await q.get()
            await self._async_launch(rockets)
            q.task_done()

    async def first_launch_rockets_with_lower_delay(self, q: asyncio.Queue):
        while True:
            rockets = await q.get()
            rockets.sort(key=lambda rocket: rocket.delay)
            await self._async_launch(rockets)
            q.task_done()


async def rocket_supplier(q: asyncio.Queue):
    while True:
        rockets_count = 10
        rockets = [Rocket() for _ in range(rockets_count)]
        await q.put(rockets)
        await asyncio.sleep(20)


async def main():
    sp = Spaceport()
    q = asyncio.Queue(maxsize=1)
    producers = [asyncio.create_task(rocket_supplier(q))]
    consumers = [asyncio.create_task(sp.launch_rockets(q))]
    await asyncio.gather(*producers)
    await q.join()
    for c in consumers:
        c.cancel()


if __name__ == '__main__':
    asyncio.run(main())
