from pyartnet import ArtNetNode
import asyncio

node = ArtNetNode('2.0.0.2')
# define universe and channels globally
universe0 = node.add_universe(0)
universe1 = node.add_universe(1)
universe2 = node.add_universe(2)
universe3 = node.add_universe(3)

channel_a = universe0.add_channel(start=1, width=24)
channel_b = universe0.add_channel(start=25, width=24)
channel_c = universe0.add_channel(start=49, width=24)
channel_d = universe0.add_channel(start=73, width=23)
# omdat strip 2 bovenaan begint keer ik expres de namen van de channels om
channel_h = universe0.add_channel(start=97, width=24)
channel_g = universe0.add_channel(start=121, width=24)
channel_f = universe0.add_channel(start=145, width=25)
channel_e = universe1.add_channel(start=1, width=23)
# strip 3 begint weer onderaan
channel_i = universe1.add_channel(start=24, width=24)
channel_j = universe1.add_channel(start=48, width=24)
channel_k = universe1.add_channel(start=72, width=24)
channel_l = universe1.add_channel(start=96, width=22)
#strip 4 begint bovenaan
channel_p = universe2.add_channel(start=1, width=24)
channel_o = universe2.add_channel(start=25, width=24)
channel_n = universe2.add_channel(start=49, width=24)
channel_m = universe2.add_channel(start=73, width=23)
# strip 5 begint weer onderaan
channel_q = universe2.add_channel(start=97, width=24)
channel_r = universe2.add_channel(start=121, width=24)
channel_s = universe2.add_channel(start=145, width=25)
channel_t = universe3.add_channel(start=1, width=23)
# strip 6 begint bovenaan
channel_x = universe3.add_channel(start=24, width=24)
channel_w = universe3.add_channel(start=48, width=24)
channel_v = universe3.add_channel(start=72, width=24)
channel_u = universe3.add_channel(start=96, width=22)


#async def blackout():

 #   channel = universe.add_channel(start=0, width=510)
 #   channel.add_fade

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

    await channel_a.wait_till_fade_complete()
    
    #channel.add_fade([0,0,0,0,0,0], timer4)
    #channel1.add_fade([0,0,0,0,0,0], timer3)
    #channel2.add_fade([0,0,0,0,0,0], timer2)
    #channel3.add_fade([0,0,0,0,0,0], timer1)


    await channel_a.wait_till_fade_complete()

asyncio.run(functie())
