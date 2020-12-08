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

#strip 1 
channela0 = universe0.add_channel(start=1, width=15)
channela1 = universe0.add_channel(start=16, width=15)
channela2 = universe0.add_channel(start=31, width=15)
channela3 = universe0.add_channel(start=46, width=15)
channela4 = universe0.add_channel(start=61, width=15)
channela5 = universe0.add_channel(start=76, width=15)
channela6 = universe0.add_channel(start=91, width=15)
channela7 = universe0.add_channel(start=106, width=15)
channela8 = universe0.add_channel(start=121, width=15)
channela9 = universe0.add_channel(start=136, width=15)
channela10 = universe0.add_channel(start=151, width=15)
channela11 = universe0.add_channel(start=166, width=15)
channela12 = universe0.add_channel(start=181, width=15)
channela13 = universe0.add_channel(start=196, width=15)
channela14 = universe0.add_channel(start=211, width=15)
channela15 = universe0.add_channel(start=226, width=15)
channela16 = universe0.add_channel(start=241, width=15)
channela17 = universe0.add_channel(start=256, width=15)
channela18 = universe0.add_channel(start=271, width=15)
channela19 = universe0.add_channel(start=286, width=15)
channela20 = universe0.add_channel(start=301, width=15)
channela21 = universe0.add_channel(start=316, width=15)
channela22 = universe0.add_channel(start=331, width=15)
channela23 = universe0.add_channel(start=346, width=15)
channela24 = universe0.add_channel(start=361, width=15)
channela25 = universe0.add_channel(start=376, width=15)
channela26 = universe0.add_channel(start=391, width=15)
channela27 = universe0.add_channel(start=406, width=15)
channela28 = universe0.add_channel(start=421, width=15)
channela29 = universe0.add_channel(start=436, width=15)
channela30 = universe0.add_channel(start=451, width=15)
channela31 = universe0.add_channel(start=466, width=15)

# strip 2 
channelb1 = universe1.add_channel(start=436, width=15)
channelb2 = universe1.add_channel(start=421, width=15)
channelb3 = universe1.add_channel(start=406, width=15)
channelb4 = universe1.add_channel(start=391, width=15)
channelb5 = universe1.add_channel(start=376, width=15)
channelb6 = universe1.add_channel(start=361, width=15)
channelb7 = universe1.add_channel(start=346, width=15)
channelb8 = universe1.add_channel(start=331, width=15)
channelb9 = universe1.add_channel(start=316, width=15)
channelb10 = universe1.add_channel(start=301, width=15)
channelb11 = universe1.add_channel(start=286, width=15)
channelb12 = universe1.add_channel(start=271, width=15)
channelb13 = universe1.add_channel(start=256, width=15)
channelb14 = universe1.add_channel(start=241, width=15)
channelb15 = universe1.add_channel(start=226, width=15)
channelb16 = universe1.add_channel(start=211, width=15)
channelb17 = universe1.add_channel(start=196, width=15)
channelb18 = universe1.add_channel(start=181, width=15)
channelb19 = universe1.add_channel(start=166, width=15)
channelb20 = universe1.add_channel(start=151, width=15)
channelb21 = universe1.add_channel(start=136, width=15)
channelb22 = universe1.add_channel(start=121, width=15)
channelb23 = universe1.add_channel(start=106, width=15)
channelb24 = universe1.add_channel(start=91, width=15)
channelb25 = universe1.add_channel(start=76, width=15)
channelb26 = universe1.add_channel(start=61, width=15)
channelb27 = universe1.add_channel(start=46, width=15)
channelb28 = universe1.add_channel(start=31, width=15)
channelb29 = universe1.add_channel(start=16, width=15)
channelb30 = universe0.add_channel(start=1, width=15)
channelb30 = universe0.add_channel(start=496, width=15)
channelb31 = universe0.add_channel(start=481, width=15)

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
    channela0.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0], 1000)  
    channela1.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0], 1000)
    channela2.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0], 1000)
    channelb3.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0],  1000)
    channelb4.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0], 1000)
    channelb14.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0], 1000)
    channela18.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0], 1000)
    channelb21.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0], 1000)
    channela17.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0], 1000)
    channelb28.add_fade([255,0,0,255,0,0,255,0,0,255,0,0,255,0,0], 1000)
    
    
 
#    channel3.add_fade([0,0,255], 1000)

#    channel4.add_fade([255,0,10], 1000)
#    channel5.add_fade([255,0,10], 1000)
#    channel6.add_fade([255,0,10], 1000)
#    channel7.add_fade([255,0,10], 1000)

    # this can be used to wait till the fade is complete

    await channela0.wait_till_fade_complete()
    await channela1.wait_till_fade_complete()
    await channela2.wait_till_fade_complete()
    await channelb3.wait_till_fade_complete()
    await channelb4.wait_till_fade_complete()
    await channelb14.wait_till_fade_complete()
    await channela18.wait_till_fade_complete()
    await channelb21.wait_till_fade_complete()
    await channela17.wait_till_fade_complete()
    await channelb28.wait_till_fade_complete()
    


    # channel0.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1000)
    #channel1.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1000)
    # channel2.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1000)
    # channel3.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1000)
 #   channel4.add_fade([0,0,0], 1000)
 #   channel5.add_fade([0,0,0], 1000)
 #   channel6.add_fade([0,0,0], 1000)
 #   channel7.add_fade([0,0,0], 1000)

  # await channel0.wait_till_fade_complete()
   # await channel1.wait_till_fade_complete()
  #  await channel2.wait_till_fade_complete()
  #  await channel3.wait_till_fade_complete()

asyncio.run(functie())

