from pyartnet import ArtNetNode, DmxChannel

node = ArtNetNode('2.0.0.2')
universe = node.add_universe(0)

channel = universe.add_channel(start=1, width=3)

def cb(ch: DmxChannel):
    ch.add_fade([0] if ch.get_channel_values() == [255] else [255], 1000)

channel.callback_fade_finished = cb
channel.callback_value_changed = my_func2
