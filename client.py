import numpy as np
import matplotlib.pyplot as plt
from encode_decode import *


class Client:
    def __init__(self):
        self.connection_socket = socket.socket()
        self.host = ''
        self.port = 0000
        self.conn = ''
        self.address = ''

        self.text_message = ''
        self.caesar = ''
        self.ascii_message = ''
        self.binary_message = ''
        self.plot_message = ''
        self.encoded_message = ''

        self.is_host = False

    def connect(self):
        self.connection_socket.connect((self.host, self.port))

    def create_connection(self):
        self.connection_socket.bind((self.host, self.port))
        self.connection_socket.listen(2)
        self.conn, self.address = self.connection_socket.accept()

    def set_message_to_send(self, message):
        self.text_message = message
        self.caesar = caesar(self.text_message, 5, 1)
        self.ascii_message = asciiEncode(self.caesar)
        self.binary_message = binaryEncode(self.ascii_message)
        self.encoded_message = Encode8B6T(self.binary_message)

    def send_message(self):

        bit_array = []
        plot_data = self.encoded_message

        for bit in plot_data:
            if bit == '+':
                bit_array.append(1)
            elif bit == '-':
                bit_array.append(-1)
            else:
                bit_array.append(0)

        if plt.fignum_exists(True):
            plt.close()

        self.plot_graph(bit_array, 'Enviado')
        if self.is_host:
            self.conn.send(self.encoded_message.encode())
        else:
            self.connection_socket.send(self.encoded_message.encode())

    def receive_message(self):
        if self.is_host:
            line_code = self.conn.recv(1024).decode()
        else:
            line_code = self.connection_socket.recv(1024).decode()

        bit_array = []
        plot_data = list(''.join(line_code))
        for bit in plot_data:
            if bit == '+':
                bit_array.append(1)
            elif bit == '-':
                bit_array.append(-1)
            else:
                bit_array.append(0)

        if plt.fignum_exists(True):
            plt.close()

        self.plot_graph(bit_array, 'Recebido')

        self.encoded_message = line_code
        self.binary_message = Decode8B6T(self.encoded_message)
        self.ascii_message = binaryDecode(self.binary_message)
        self.caesar = asciiDecode(self.ascii_message)
        self.text_message = caesar(self.caesar, 5, 0)

    def plot_graph(self, message, title):
        if plt.fignum_exists(True):
            plt.close()
        plt.rcParams["figure.autolayout"] = True
        plt.title(title)
        index = list(np.arange(len(message)))
        plt.hlines(y = 0, xmin = 0, xmax = len(message), linewidth = 1)
        plt.bar(index, message)
        plt.show()
