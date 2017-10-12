import sys
import os
sys.path.append("..")
print sys.path
from neighbor_discovery import NeighborDiscover
from nose.tools import assert_equals
from Message import Message
from HalfBlockDatabase import HalfBlock,HalfBlockDatabase
from crypto import ECCrypto
from hashlib import sha1
import logging
BASE = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Test_HalfBlockDatabase:
    def setup(self):
        print ("TestUM:setup() before each test method")
        self.crypto = ECCrypto()
        self.my_key1 = self.crypto.generate_key(u"medium")
        self.my_key2 = self.crypto.generate_key(u"medium")
        self.my_key3 = self.crypto.generate_key(u"medium")
        self.my_key4 = self.crypto.generate_key(u"medium")
        self.my_key5 = self.crypto.generate_key(u"medium")
        self.my_key6 = self.crypto.generate_key(u"medium")

        self.my_identity1 = self.crypto.key_to_hash(self.my_key1.pub())
        self.my_identity2 = self.crypto.key_to_hash(self.my_key2.pub())
        self.my_identity3 = self.crypto.key_to_hash(self.my_key3.pub())
        self.my_identity4 = self.crypto.key_to_hash(self.my_key4.pub())
        self.my_identity5 = self.crypto.key_to_hash(self.my_key5.pub())
        self.my_identity6 = self.crypto.key_to_hash(self.my_key6.pub())


        self.my_public_key1 = self.crypto.key_to_bin(self.my_key1.pub())
        self.my_public_key2 = self.crypto.key_to_bin(self.my_key2.pub())
        self.my_public_key3 = self.crypto.key_to_bin(self.my_key3.pub())
        self.my_public_key4 = self.crypto.key_to_bin(self.my_key4.pub())
        self.my_public_key5 = self.crypto.key_to_bin(self.my_key5.pub())
        self.my_public_key6 = self.crypto.key_to_bin(self.my_key6.pub())


        if os.path.isfile('BlockDataBase.db'):
            os.remove('BlockDataBase.db')
        self.database = HalfBlockDatabase(os.path.join(BASE, 'BlockDataBase.db'))
    def teardown(self):
        print ("TestUM:teardown() after each test method")

    @classmethod
    def setup_class(cls):
        print ("setup_class() before any methods in this class")
        #cls.walker = Walker(port=23334)

    @classmethod
    def teardown_class(cls):
        print ("teardown_class() after any methods in this class")

    def test_add_and_get_member(self):
        self.database.add_member(identity=self.my_identity1,public_key=self.my_public_key1)
        result = self.database.get_member(public_key=self.my_public_key1)
        assert str(result[0])==self.my_identity1
        assert str(result[1])==self.my_public_key1

    def test_add_and_get_block(self):

        block1 = HalfBlock()
        block1.public_key = self.my_public_key1

        block2 = HalfBlock()
        block2.public_key = self.my_public_key2
        self.database.add_block(block1)
        self.database.add_block(block2)

        blocks = self.database.get_blocks_by_public_key(public_key = self.my_public_key1)
        for block in blocks:
            if block.public_key == self.my_public_key1:
                block.insert_time=block1.insert_time
                assert block.insert_time == block1.insert_time
            if block.public_key == self.my_public_key2:
                block.insert_time=block2.insert_time
                assert block == block2
    def test_has_block(self):
        block3 = HalfBlock()
        block3.public_key = self.my_public_key3

        block4 = HalfBlock()
        block4.public_key = self.my_public_key4
        self.database.add_block(block3)
        status1 = self.database.has_block(block3)
        status2 = self.database.has_block(block4)

        assert status1 == True
        assert status2 == False

    def test_get_all_member(self):
        self.database.add_member(identity=self.my_identity1,public_key=self.my_public_key1)
        self.database.add_member(identity=self.my_identity2,public_key=self.my_public_key2)
        members = self.database.get_all_member()
        assert members != None


    def test_get_latest_sequence_number(self):
        block3 = HalfBlock()
        block3.public_key = self.my_public_key3
        block3.sequence_number = 1

        block4 = HalfBlock()
        block4.public_key = self.my_public_key3
        block4.sequence_number = 2

        self.database.add_block(block3)
        self.database.add_block(block4)
        sequence_number = self.database.get_latest_sequence_number(public_key=self.my_public_key3)
        assert sequence_number == 2

    def test_get_blocks_since(self):
        block1 = HalfBlock()
        block1.public_key = self.my_public_key4
        block1.sequence_number=1

        block2 = HalfBlock()
        block2.public_key = self.my_public_key4
        block2.sequence_number=2

        self.database.add_block(block1)
        self.database.add_block(block2)
        blocks = self.database.get_blocks_since(sequence_number=2,public_key=self.my_public_key4)

        assert blocks[0].public_key == self.my_public_key4
        assert blocks[0].sequence_number == 2


    def test_get_blocks_by_public_key(self):
        block = HalfBlock()
        block.public_key = "haha"
        block.sequence_number =80
        self.database.add_block(block)
        block_return = self.database.get_blocks_by_public_key(public_key="haha")
        assert block_return[0].public_key=="haha"
        assert block_return[0].sequence_number == 80

    def test_add_and_get_visit_record(self):
        self.database.add_visit_record(ip="6.6.6.6",port=6,public_key="haha2")
        results = self.database.get_all_visit_records()
        print("it is:")
        print str(results[0][0])
        assert str(results[0][0]) == "6.6.6.6"
        assert results[0][1] == 6
        assert str(results[0][2]) == "haha2"


