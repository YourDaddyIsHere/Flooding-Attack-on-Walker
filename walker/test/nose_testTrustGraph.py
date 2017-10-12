import sys
import os
sys.path.append("..")
print sys.path
from nose.tools import assert_equals
from database import Block
from database import Trusted_Walker_Database
from crypto import ECCrypto
from hashlib import sha1
from database import TrustGraph
import logging

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Test_Message:
    def setup(self):
        print ("TestUM:setup() before each test method")
        self.crypto = ECCrypto()
        self.my_key1 = self.crypto.generate_key(u"medium")
        self.my_key2 = self.crypto.generate_key(u"medium")
        self.my_key3 = self.crypto.generate_key(u"medium")
        self.my_key4 = self.crypto.generate_key(u"medium")
        self.my_key5 = self.crypto.generate_key(u"medium")

        self.my_identity1 = self.crypto.key_to_hash(self.my_key1.pub())
        self.my_identity2 = self.crypto.key_to_hash(self.my_key2.pub())
        self.my_identity3 = self.crypto.key_to_hash(self.my_key3.pub())
        self.my_identity3 = self.crypto.key_to_hash(self.my_key4.pub())
        self.my_identity3 = self.crypto.key_to_hash(self.my_key5.pub())

        self.my_public_key1 = self.crypto.key_to_bin(self.my_key1.pub())
        self.my_public_key2 = self.crypto.key_to_bin(self.my_key2.pub())
        self.my_public_key3 = self.crypto.key_to_bin(self.my_key3.pub())
        self.my_public_key4 = self.crypto.key_to_bin(self.my_key4.pub())
        self.my_public_key5 = self.crypto.key_to_bin(self.my_key5.pub())
        """
        if os.path.isfile('BlockDataBase.db'):
            os.remove('BlockDataBase.db')
        self.database = Trusted_Walker_Database()
        """

        self.block1 = Block()
        self.block1.init(public_key_requester=self.my_public_key1,public_key_responder=self.my_public_key2,up=200,down=300,total_up_requester=3,total_down_requester=4,
                      sequence_number_requester=5,previous_hash_requester="h1",signature_requester="s1",total_up_responder=8,
                      total_down_responder=9,sequence_number_responder=10,previous_hash_responder="h2",signature_responder="s2")

        self.block2 = Block()
        self.block2.init(public_key_requester=self.my_public_key2,public_key_responder=self.my_public_key3,up=500,down=0,total_up_requester=3,total_down_requester=4,
                      sequence_number_requester=5,previous_hash_requester="h1",signature_requester="s1",total_up_responder=8,
                      total_down_responder=9,sequence_number_responder=10,previous_hash_responder="h2",signature_responder="s2")

        self.block3 = Block()
        self.block3.init(public_key_requester=self.my_public_key4,public_key_responder=self.my_public_key2,up=600,down=0,total_up_requester=3,total_down_requester=4,
                      sequence_number_requester=5,previous_hash_requester="h1",signature_requester="s1",total_up_responder=8,
                      total_down_responder=9,sequence_number_responder=10,previous_hash_responder="h2",signature_responder="s2")

        #self.TG = TrustGraph()

    def teardown(self):
        print ("TestUM:teardown() after each test method")

    @classmethod
    def setup_class(cls):
        print ("setup_class() before any methods in this class")
        #cls.walker = Walker(port=23334)

    @classmethod
    def teardown_class(cls):
        print ("teardown_class() after any methods in this class")

    def test_add_edge(self):
        TG = TrustGraph()
        TG.add_block(self.block1)
        assert TG.Graph[self.my_public_key1][self.my_public_key2]["weight"] == self.block1.up
        assert TG.Graph[self.my_public_key2][self.my_public_key1]["weight"] == self.block1.down
    def test_has_trust_path(self):
        TG = TrustGraph()
        TG.add_block(self.block1)
        TG.add_block(self.block2)
        TG.add_block(self.block3)
        #TG.draw_graph()
        assert TG.has_trust_path(your_node=self.my_public_key4,node_to_be_trusted=self.my_public_key1)==False
        assert TG.has_trust_path(your_node=self.my_public_key1,node_to_be_trusted=self.my_public_key4)==True
        assert TG.has_trust_path(your_node=self.my_public_key3,node_to_be_trusted=self.my_public_key4)==True

    def test_error(self):
        assert 1>2