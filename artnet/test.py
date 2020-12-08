from pyartnet import ArtNetNode
import asyncio
import time

#dit stukje is om de dmx nodes aan te geven 
node0 = ArtNetNode('2.0.0.2')
node1= ArtNetNode('2.0.0.2')
node2= ArtNetNode('2.0.0.2')
node3= ArtNetNode('2.0.0.2')
universe0 = node0.add_universe(0)
universe1 = node1.add_universe(1)
universe2 = node2.add_universe(2)
universe3 = node3.add_universe(3)


channel0 = universe0.add_channel(start=1, width=15)
channel1 = universe1.add_channel(start=1, width=15)
channel2 = universe2.add_channel(start=1, width=15)
channel3 = universe3.add_channel(start=1, width=15)


async def functie():
#hier starten we de 4 nodes 
    await node0.start()
    await node1.start()
    await node2.start()
    await node3.start()

#    universe0 = node.add_universe(2,1)
 #GG   universe1 = node.add_universe(0)
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

#width 3 = 1 LED!
#    channel  = universe0.add_channel(start=1, width=15)
#    channel1 = universe1.add_channel(start=40, width=15)
#    channel2 = universe.add_channel(start=7, width=3)
#    channel3 = universe.add_channel(start=10, width=3)

#    channel4 = multiverse.add_channel(start=1, width=3)
#    channel5 = multiverse.add_channel(start=10, width=3)
#    channel6 = multiverse.add_channel(start=20, width=3)
#    channel7 = multiverse.add_channel(start=40, width=3)

    # Fade channel to 255,0,0 in 5s
    # The fade will automatically run in the background
    channel0.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0], 1000)  
    channel1.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0], 1000)
    channel2.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0], 1000)
    channel3.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0],  1000)
#    channel3.add_fade([0,0,255], 1000)

#    channel4.add_fade([255,0,10], 1000)
#    channel5.add_fade([255,0,10], 1000)
#    channel6.add_fade([255,0,10], 1000)
#    channel7.add_fade([255,0,10], 1000)

    # this can be used to wait till the fade is complete

    await channel0.wait_till_fade_complete()
    await channel1.wait_till_fade_complete()
    await channel2.wait_till_fade_complete()
    await channel3.wait_till_fade_complete()


    channel0.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1000)
    channel1.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1000)
    channel2.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1000)
    channel3.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1000)
 #   channel4.add_fade([0,0,0], 1000)
 #   channel5.add_fade([0,0,0], 1000)
 #   channel6.add_fade([0,0,0], 1000)
 #   channel7.add_fade([0,0,0], 1000)

    await channel0.wait_till_fade_complete()
    await channel1.wait_till_fade_complete()
    await channel2.wait_till_fade_complete()
    await channel3.wait_till_fade_complete()

asyncio.run(functie())

