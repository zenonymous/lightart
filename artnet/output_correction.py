from pyartnet import ArtNetNode, output_correction

node = ArtNetNode('2.0.0.2')

universe = node.add_universe(0)
universe.output_correction = output_correction.quadratic  # quadratic will be used for all channels

channel = universe.add_channel(start=1, width=3)
channel.output_correction = output_correction.cubic       # this channel will use cubic
