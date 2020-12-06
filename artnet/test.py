from pyartnet import ArtNetNode
import asyncio
import time
node = ArtNetNode('2.0.0.255')
async def functie():
    await node.start()

    universe = node.add_universe(0)
    multiverse = node.add_universe(1)
    # dit zou een range van channels kunnen requesten
    # channel = universe.get_channel('1/3')  
#    cnr = 1
#    StartOfChannel = 1
#    for x in range(170):
#    channel

# universe 0 led 1 begint bij adres 1, en gaat tot 170
# universe 1 led 1 begint bij adres 1, en gaat tot 118 leds (*3) 
# universe 2 led 1 begint bij adres 1, en gaat tot 170
# universe 3 led 1 begint bij adres 1, en gaat tot 118 leds (*3)

# strip 1 is 1 (onderaan paal) tot 96
# strip 2 is 97 (bovenaan paal) tot 193 
# strip 3 is 194 (begint onderaan) tot 288
# repeat tot strip 6
    channel  = universe.add_channel(start=1, width=3)
    channel1 = universe.add_channel(start=4, width=3)
    channel2 = universe.add_channel(start=7, width=3)
    channel3 = universe.add_channel(start=10, width=3)

    channel4 = multiverse.add_channel(start=1, width=3)
    channel5 = multiverse.add_channel(start=10, width=3)
    channel6 = multiverse.add_channel(start=20, width=3)
    channel7 = multiverse.add_channel(start=40, width=3)

    # Fade channel to 255,0,0 in 5s
    # The fade will automatically run in the background
    channel.add_fade([0,0,255], 1000)  
    channel1.add_fade([0,0,255], 1000)
    channel2.add_fade([0,0,255], 1000)
    channel3.add_fade([0,0,255], 1000)

    channel4.add_fade([255,0,10], 1000)
    channel5.add_fade([255,0,10], 1000)
    channel6.add_fade([255,0,10], 1000)
    channel7.add_fade([255,0,10], 1000)

    # this can be used to wait till the fade is complete

    await channel.wait_till_fade_complete()
    
    channel.add_fade([0,0,0], 1000)
    channel1.add_fade([0,0,0], 1000)
    channel2.add_fade([0,0,0], 1000)
    channel3.add_fade([0,0,0], 1000)
    channel4.add_fade([0,0,0], 1000)
    channel5.add_fade([0,0,0], 1000)
    channel6.add_fade([0,0,0], 1000)
    channel7.add_fade([0,0,0], 1000)

    await channel1.wait_till_fade_complete()

asyncio.run(functie())
