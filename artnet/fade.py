from pyartnet import ArtNetNode
import asyncio
import random

node = ArtNetNode('2.0.0.2')
async def functie():
    await node.start()

    universe = node.add_universe(0)

    # dit zou een range van channels kunnen requesten
    # channel = universe.get_channel('1/3')  
    one = random.randint(0,500)
    two = random.randint(0,500)
    three = random.randint(0, 500)
    four = random.randint(0, 500)
    channel  = universe.add_channel(start=one, width=6)
    channel1 = universe.add_channel(start=two, width=6)
    channel2 = universe.add_channel(start=three, width=6)
    channel3 = universe.add_channel(start=four, width=6)


    ha = random.randint(0,25)
    ja = random.randint(0,25)


    # Fade channel to 255,0,0 in 5s
    # The fade will automatically run in the background
    channel.add_fade([ha,ja,0,5,3,2], 2000)   
    channel1.add_fade([255,23,0,5,4,2], 2000)
    channel2.add_fade([0,255,23,43,6,9], 3000)
    channel3.add_fade([35,92,37,34,54,24], 3000)
    # this can be used to wait till the fade is complete

    await channel.wait_till_fade_complete()
    
    channel.add_fade([0,0,0,0,0,0], 3000)
    channel1.add_fade([0,0,0,0,0,0], 5000)
    channel2.add_fade([0,0,0,0,0,0], 4000)
    channel3.add_fade([0,0,0,0,0,0], 1000)

    await channel1.wait_till_fade_complete()

asyncio.run(functie())
