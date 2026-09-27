from pyartnet import ArtNetNode
import asyncio
import random

node = ArtNetNode('2.0.0.2')
async def functie():
    await node.start()

    universe = node.add_universe(0)
    multiverse = node.add_universe(1)
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

    channel4 = multiverse.add_channel(start=four, width=6)
    channel5 = multiverse.add_channel(start=three, width=6)
    channel6 = multiverse.add_channel(start=two, width=6)
    channel7 = multiverse.add_channel(start=one, width=6)

    ha = random.randint(0,25)
    ja = random.randint(0,25)
    bla = random.randint(0,50)

    timer1 = random.randint(0,4000)
    timer2 = random.randint(0,5000)
    timer3 = random.randint(0,6000)
    timer4 = random.randint(0,2000)

    # Fade channel to 255,0,0 in 5s
    # The fade will automatically run in the background
    channel.add_fade([ha,ja,0,bla,3,2], timer1)   
    channel1.add_fade([255,23,ja,5,bla,2], timer2)
    channel2.add_fade([ha,255,bla,43,6,9], timer3)
    channel3.add_fade([35,ja,37,34,bla,24], timer4)

    channel4.add_fade([ja,255,ha,bla,ja,ha], timer4)
    channel5.add_fade([bla,ha,123,bla,ha,ja], timer3)
    channel6.add_fade([ja,ha,bla,111,ha,bla], timer2)
    channel7.add_fade([23,bla,ja,ja,ha,ha], timer1)

    # this can be used to wait till the fade is complete

    await channel.wait_till_fade_complete()
    
    channel.add_fade([0,0,0,0,0,0], timer4)
    channel1.add_fade([0,0,0,0,0,0], timer3)
    channel2.add_fade([0,0,0,0,0,0], timer2)
    channel3.add_fade([0,0,0,0,0,0], timer1)
    channel4.add_fade([0,0,0,0,0,0], timer1)
    channel5.add_fade([0,0,0,0,0,0], timer2)
    channel6.add_fade([0,0,0,0,0,0], timer3)
    channel7.add_fade([0,0,0,0,0,0], timer4)

    await channel1.wait_till_fade_complete()

asyncio.run(functie())
