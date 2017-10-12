import sys
import os
sys.path.append("..")
print sys.path
from twisted.internet import reactor
from Neighbor import Neighbor
from Neighbor_group import NeighborGroup
import time
from neighbor_discovery import NeighborDiscover
from Message import Message

#logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",format="%(asctime)-15s %(levelname)-8s %(message)s")
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

class TestNeighborDiscovery:
    def setup(self):
        print ("TestUM:setup() before each test method")
        #self.neighbor_discovery = NeighborDiscover(is_tracker=True)
        self.neighbor_group = NeighborGroup()
        self.neighbors = []
        self.reactor=reactor
        for i in range(0,6):
            neighbor = Neighbor(private_address=("1.1.1.1",i),public_address=("2.2.2.2",i))
            self.neighbors.append(neighbor)
            #reactor.callLater(1,self.test_on_introduction_response)
            #reactor.callLater(5,self.stop)
        #self.neighbor_discovery.run()
        #self.neighbor_discovery.reactor.run()
    def teardown(self):
        print ("TestUM:teardown() after each test method")

    @classmethod
    def setup_class(cls):
        print ("setup_class() before any methods in this class")
        #cls.walker = Walker(port=23334)

    @classmethod
    def teardown_class(cls):
        print ("teardown_class() after any methods in this class")

    """
    def stop(self):
        if self.neighbor_discovery.reactor.running:
            self.neighbor_discovery.reactor.callFromThread(self.neighbor_discovery.reactor.stop)
    """
    def stop_reactor(self):
        pass


    def test_on_introduction_response(self):
        neighbor_discovery = NeighborDiscover(is_tracker=True)
        message_response1 = Message(neighbor_discovery=neighbor_discovery,identifier=1,destination_address=("0.0.0.1",8),source_private_address=("8.8.8.1",8),source_public_address=("8.8.8.2",8),
                                    private_introduction_address=("6.6.6.1",6),public_introduction_address=("6.6.6.2",6))
        message_response1.encode_introduction_response()

        message_response2 = Message(neighbor_discovery=neighbor_discovery,identifier=2,destination_address=("0.0.0.1",8),source_private_address=("5.5.5.1",5),source_public_address=("5.5.5.2",5),
                                    private_introduction_address=("7.7.7.1",7),public_introduction_address=("7.7.7.2",7))
        message_response2.encode_introduction_response()

        message_response3 = Message(neighbor_discovery=neighbor_discovery,identifier=3,destination_address=("0.0.0.1",8),source_private_address=("6.6.6.1",6),source_public_address=("6.6.6.2",6),
                                    private_introduction_address=("7.7.7.1",7),public_introduction_address=("7.7.7.2",7))
        message_response3.encode_introduction_response()

        neighbor_discovery.on_introduction_response(packet=message_response1.packet,addr=("8.8.8.2",8))
        print("start asserts")
        #assert False
        assert neighbor_discovery.neighbor_group.current_neighbor.get_public_address()==("6.6.6.2",6)
        neighbor_discovery.on_introduction_response(packet=message_response2.packet,addr=("8.8.8.2",8))

        assert neighbor_discovery.neighbor_group.current_neighbor.get_public_address()==("6.6.6.2",6)

        neighbor_discovery.on_introduction_response(packet=message_response3.packet,addr=("6.6.6.2",6))
        print("the current neighbor is:")
        print neighbor_discovery.neighbor_group.current_neighbor.get_public_address()
        print neighbor_discovery.neighbor_group.current_neighbor.get_private_address()
        assert neighbor_discovery.neighbor_group.current_neighbor.get_public_address()==("7.7.7.2",7)