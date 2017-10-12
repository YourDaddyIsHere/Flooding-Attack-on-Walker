import sys
import os
sys.path.append("..")
print sys.path

from Neighbor import Neighbor

#logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",format="%(asctime)-15s %(levelname)-8s %(message)s")
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

class Test_Neighbor:
    def setup(self):
        print ("TestUM:setup() before each test method")
        self.neighbor = Neighbor(private_address=("1.1.1.1",1),public_address=("2.2.2.2",2))
    def teardown(self):
        print ("TestUM:teardown() after each test method")

    @classmethod
    def setup_class(cls):
        print ("setup_class() before any methods in this class")
        #cls.walker = Walker(port=23334)

    @classmethod
    def teardown_class(cls):
        print ("teardown_class() after any methods in this class")

    def test_get_private_address(self):
        private_address_test = self.neighbor.get_private_address()
        assert private_address_test==("1.1.1.1",1)
    def test_get_private_ip(self):
        private_ip_test = self.neighbor.get_private_ip()
        assert private_ip_test == "1.1.1.1"
    def test_get_public_ip(self):
        public_ip_test = self.neighbor.get_public_ip()
        assert public_ip_test =="2.2.2.2"
    def test_get_public_port(self):
        public_port_test = self.neighbor.get_public_port()
        assert public_port_test == 2

