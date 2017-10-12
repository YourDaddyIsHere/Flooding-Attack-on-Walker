from walker.neighbor_discovery import NeighborDiscover
from twisted.internet import reactor
walker = NeighborDiscover(is_tracker=True)
reactor.run()