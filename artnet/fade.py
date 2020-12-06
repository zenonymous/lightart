from pyartnet import ArtNetNode
import asyncio


node = ArtNetNode('2.0.0.2')
async def functie():
    await node.start()

    universe = node.add_universe(0)

    # dit zou een range van channels kunnen requesten
    # channel = universe.get_channel('1/3')   
    channel  = universe.add_channel(start=1, width=3)

    # Fade channel to 255,0,0 in 5s
    # The fade will automatically run in the background
    channel.add_fade([255,0,0], 5000)   

    # this can be used to wait till the fade is complete

    await channel.wait_till_fade_complete()

asyncio.run(functie())

