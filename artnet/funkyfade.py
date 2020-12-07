from pyartnet import ArtNetNode
import asyncio

node = ArtNetNode('2.0.0.2')
# define universe and channels globally
universe0 = node.add_universe(0)
universe1 = node.add_universe(1)
universe2 = node.add_universe(2)
universe3 = node.add_universe(3)

strip1_a = universe0.add_channel(start=1, width=24)
strip1_b = universe0.add_channel(start=25, width=24)
strip1_c = universe0.add_channel(start=49, width=24)
strip1_d = universe0.add_channel(start=73, width=23)
# omdat strip 2 bovenaan begint keer ik expres de namen van de channels om
strip2_d = universe0.add_channel(start=97, width=24)
strip2_c = universe0.add_channel(start=121, width=24)
strip2_b = universe0.add_channel(start=145, width=25)
strip2_a = universe1.add_channel(start=1, width=23)
# strip 3 begint weer onderaan
strip3_a = universe1.add_channel(start=24, width=24)
strip3_b = universe1.add_channel(start=48, width=24)
strip3_c = universe1.add_channel(start=72, width=24)
strip3_d = universe1.add_channel(start=96, width=22)
#strip 4 begint bovenaan
strip4_d = universe2.add_channel(start=1, width=24)
strip4_c = universe2.add_channel(start=25, width=24)
strip4_b = universe2.add_channel(start=49, width=24)
strip4_a = universe2.add_channel(start=73, width=23)
# strip 5 begint weer onderaan
strip5_a = universe2.add_channel(start=97, width=24)
strip5_b = universe2.add_channel(start=121, width=24)
strip5_c = universe2.add_channel(start=145, width=25)
strip5_d = universe3.add_channel(start=1, width=23)
# strip 6 begint bovenaan
strip6_d = universe3.add_channel(start=24, width=24)
strip6_c = universe3.add_channel(start=48, width=24)
strip6_b = universe3.add_channel(start=72, width=24)
strip6_a = universe3.add_channel(start=96, width=22)

#async def blackout():

 #   channel = universe.add_channel(start=0, width=510)
 #   channel.add_fade

async def strips_a(color, timer):
    await node.start()

    strip1_a.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip2_a.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip3_a.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip4_a.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip5_a.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip6_a.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], timer)

    await strip1_a.wait_till_fade_complete()

async def blackout_strips_a(timer):
    await node.start()

    strip1_a.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip2_a.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip3_a.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip4_a.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip5_a.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip6_a.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], timer)

    await strip1_a.wait_till_fade_complete()

async def strips_b(color, timer):
    await node.start()

    strip1_b.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip2_b.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip3_b.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip4_b.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip5_b.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip6_b.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)

    await strip1_b.wait_till_fade_complete()

async def blackout_strips_b(timer):
    await node.start()

    strip1_b.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip2_b.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip3_b.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip4_b.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip5_b.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip6_b.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)

    await strip1_b.wait_till_fade_complete()

async def strips_c(color, timer):
    await node.start()

    strip1_c.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip2_c.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip3_c.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip4_c.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip5_c.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip6_c.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)

    await strip1_c.wait_till_fade_complete()

async def blackout_strips_c(timer):
    await node.start()

    strip1_c.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip2_c.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip3_c.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip4_c.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip5_c.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip6_c.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)

    await strip1_c.wait_till_fade_complete()

async def strips_d(color, timer):
    await node.start()

    strip1_d.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip2_d.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip3_d.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip4_d.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip5_d.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip6_d.add_fade([color,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], timer)

    await strip1_d.wait_till_fade_complete()

async def blackout_strips_d(timer):
    await node.start()

    strip1_d.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip2_d.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip3_d.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip4_d.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip5_d.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], timer)
    strip6_d.add_fade([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,], timer)

    await strip1_d.wait_till_fade_complete()

async def functie():
    await node.start()

  #  universe = node.add_universe(0)
    # dit zou een range van channels kunnen requesten
    # channel = universe.get_channel('1/3')  
    #channel  = universe.add_channel(start=one, width=6)
    #channel1 = universe.add_channel(start=two, width=6)
    #channel2 = universe.add_channel(start=three, width=6)
    #channel3 = universe.add_channel(start=four, width=6)



    # Fade channel to 255,0,0 in 5s
    # The fade will automatically run in the background
    #channel.add_fade([ha,ja,0,bla,3,2], timer1)   
    #channel1.add_fade([255,23,ja,5,bla,2], timer2)
    #channel2.add_fade([ha,255,bla,43,6,9], timer3)
    #channel3.add_fade([35,ja,37,34,bla,24], timer4)

    # this can be used to wait till the fade is complete

    await strip1_a.wait_till_fade_complete()
    
    #channel.add_fade([0,0,0,0,0,0], timer4)
    #channel1.add_fade([0,0,0,0,0,0], timer3)
    #channel2.add_fade([0,0,0,0,0,0], timer2)
    #channel3.add_fade([0,0,0,0,0,0], timer1)


    await strip1_a.wait_till_fade_complete()


#asyncio.run(start())
#asyncio.run(functie())
asyncio.run(strips_a(255, 1000))
#asyncio.run(strips_a(0, 1000))
#asyncio.run(blackout_strips_a(1000))
asyncio.run(strips_b(255, 1000))
#asyncio.run(strips_c(255, 1000))
#asyncio.run(strips_d(255, 1000))
