import sys
import os
sys.path.append("..")
print sys.path

from Neighbor import Neighbor
from Neighbor_group import NeighborGroup
import time

#logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",format="%(asctime)-15s %(levelname)-8s %(message)s")
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

class TestNeighborGroup:
    def setup(self):
        print ("TestUM:setup() before each test method")
        self.neighbor_group = NeighborGroup()
        self.neighbors = []
        for i in range(0,6):
            neighbor = Neighbor(private_address=("1.1.1.1",i),public_address=("2.2.2.2",i))
            self.neighbors.append(neighbor)
    def teardown(self):
        print ("TestUM:teardown() after each test method")

    @classmethod
    def setup_class(cls):
        print ("setup_class() before any methods in this class")
        #cls.walker = Walker(port=23334)

    @classmethod
    def teardown_class(cls):
        print ("teardown_class() after any methods in this class")

    def test_choose_group(self):
        (group_name,group)=self.neighbor_group.choose_group()
        assert group_name in ["tracker","trusted neighbor","outgoing","incoming","intro"]

    def test_getneighbor_to_walk(self):
        self.neighbor_group.teleport_home_possibility=0
        self.neighbor_group.update_current_neighbor(responder=self.neighbors[4],introduced_neighbor=self.neighbors[5])
        neighbor = self.neighbor_group.get_neighbor_to_walk()
        print("the neighbor to walk is:")
        print neighbor.get_private_address()
        assert self.neighbor_group.is_same_neighbor(self.neighbor_group.current_neighbor,self.neighbors[5])

    def test_is_in_list(self):
        self.neighbor_group.outgoing_neighbors.append(self.neighbors[0])
        assert self.neighbor_group.is_in_list(self.neighbors[0],self.neighbor_group.outgoing_neighbors) == True
        assert self.neighbor_group.is_in_list(self.neighbors[1],self.neighbor_group.outgoing_neighbors) == False

    def test_is_same_neighbor(self):
        assert self.neighbor_group.is_same_neighbor(self.neighbors[0],self.neighbors[0]) == True
        assert self.neighbor_group.is_same_neighbor(self.neighbors[0],self.neighbors[1]) == False

    def test_associate_neigbhor_with_public_key(self):
        self.neighbor_group.tracker.append(self.neighbors[0])
        self.neighbor_group.incoming_neighbors.append(self.neighbors[0])
        self.neighbor_group.outgoing_neighbors.append(self.neighbors[0])
        self.neighbor_group.associate_neigbhor_with_public_key(private_ip = self.neighbors[0].get_private_ip(),public_ip = self.neighbors[0].get_public_ip(),
                                                              public_key="hahaha")
        assert self.neighbor_group.tracker[0].public_key == "hahaha"
        assert self.neighbor_group.incoming_neighbors[0].public_key == "hahaha"
        assert self.neighbor_group.outgoing_neighbors[0].public_key == "hahaha"

    def test_clean_stale_neighbors(self):
        neighbor = self.neighbors[2]
        neighbor.last_outgoing_time = time.time()-60
        self.neighbor_group.add_neighbor_to_outgoing_list(self.neighbors[2])
        self.neighbor_group.add_neighbor_to_outgoing_list(self.neighbors[0])
        assert self.neighbor_group.is_in_list(self.neighbors[2],self.neighbor_group.outgoing_neighbors) == False

    def test_add_neighbor_to_outgoing_list(self):
        self.neighbor_group.add_neighbor_to_outgoing_list(self.neighbors[1])
        assert self.neighbors[1] in self.neighbor_group.outgoing_neighbors

    def test_add_neighbor_to_incoming_list(self):
        self.neighbor_group.add_neighbor_to_incoming_list(self.neighbors[1])
        assert self.neighbors[1] in self.neighbor_group.incoming_neighbors

    def test_add_neighbor_to_intro_list(self):
        self.neighbor_group.add_neighbor_to_intro_list(self.neighbors[1])
        assert self.neighbors[1] in self.neighbor_group.intro_neighbors

    def test_add_neighbor_to_trusted_list(self):
        self.neighbor_group.add_neighbor_to_trusted_list(self.neighbors[1])
        assert self.neighbors[1] in self.neighbor_group.trusted_neighbors

    def test_get_neighbor_to_walk(self):
        self.neighbor_group.get_neighbor_to_walk()

    def test_get_neighbor_to_introduce(self):
        self.neighbor_group.get_neighbor_to_introduce(self.neighbors[0])

    def test_update_current_neighbor(self):
        self.neighbor_group.update_current_neighbor(responder=self.neighbors[0],introduced_neighbor=self.neighbors[1])
        assert self.neighbor_group.is_same_neighbor(self.neighbor_group.current_neighbor,self.neighbors[1])

        self.neighbor_group.update_current_neighbor(responder=self.neighbors[0],introduced_neighbor=self.neighbors[2])
        assert self.neighbor_group.is_same_neighbor(self.neighbor_group.current_neighbor,self.neighbors[1])

        self.neighbor_group.update_current_neighbor(responder=self.neighbors[1],introduced_neighbor=self.neighbors[3])
        assert self.neighbor_group.is_same_neighbor(self.neighbor_group.current_neighbor,self.neighbors[3])

    def test_insert_trusted_neighbor(self):
        pass

