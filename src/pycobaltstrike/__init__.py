""" pycobaltstrike is a module to interact with cobaltstrike's external c2 """

import base64
import socket
import struct

__version__ = "1.0.0"


class Frame(object):
    """ represents a pycobaltstrike data frame """

    data: bytes
    size: int

    def __init__(self, data: bytes):
        self.data = data
        self.size = len(data)

    @classmethod
    def from_bytes(cls, data: bytes):
        """ init a new instance from bytes that include the size """

        return cls(data[4:])

    @classmethod
    def from_base64(cls, data: str):
        """ init a new instance from base64'd bytes that include the size """

        return cls.from_bytes(base64.b64decode(data))

    @property
    def size_bytes(self) -> bytes:
        """ get the data size as bytes """

        return struct.pack('<I', len(self.data))

    @property
    def as_bytes(self) -> bytes:
        """ get the full frame as bytes """

        return self.size_bytes + self.data

    @property
    def base64bytes(self) -> str:
        """ return a base64 rep of the full frame as bytes """

        return base64.b64encode(self.as_bytes).decode()

    def __repr__(self):
        return f'Frame<size = {self.size}, sample (hex) = {self.as_bytes[:10].hex()} ... {self.as_bytes[-10:].hex()}>'


class CobaltStrike(object):
    """ CobaltStrike is a CobaltStrike external C2 socket handler """

    port: int
    host: str
    sock: socket

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ''

        self.last_stage = None

    def connect(self, host: str, port: int):
        self.host = host
        self.port = port

        self.sock.connect((host, port))
        self.sock.settimeout(5)

    def is_connected(self):
        if self.host == '':
            return False

        return True

    def send(self, frame: Frame):
        """
            "All frames start with a 4-byte little-endian byte order integer."

            :param frame:
            :return:
        """

        self.sock.send(frame.size_bytes)
        self.sock.send(frame.data)

    def recv(self) -> Frame:
        """
            Receive a Frame from the CS External C2 socket.

            :return:
        """

        length_bytes = self.sock.recv(4)
        length = struct.unpack('<I', length_bytes)[0]

        read = 0
        data = b''
        while read < length:
            buf = self.sock.recv(1024)
            read += len(buf)
            data = data + buf

        return Frame(data)

    def get_stage(self, arch: str, pipename: str = 'beacon', block: str = "100"):
        """
            Get a Cobaltstrike stage.

            This stage is also recorded in the last_stage class property in case
            you need to get it again.

            :param arch:
            :param pipename:
            :param block:
            :return:
        """

        self.send(Frame(f'arch={arch}'.encode()))
        self.send(Frame(f'pipename={pipename}'.encode()))
        self.send(Frame(f'block={block}'.encode()))
        self.send(Frame('go'.encode()))

        self.last_stage = self.recv()

        return self.last_stage
