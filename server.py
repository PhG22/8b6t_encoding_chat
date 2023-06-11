import socket
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from encode_decode import encode, decode

if __name__ == '__main__':
    
    # informações para criar o servidor 
    host = socket.gethostname()
    port = input()  

    # instancia o socket
    server_socket = socket.socket()  
    
    # cria a conexão
    server_socket.bind((host, int(port)))  
    server_socket.listen(2)
    conn, address = server_socket.accept()  
    
    # printa as informações do cliente quando conectado
    print("Conexão de: " + str(address))
    
    while True:
        message = conn.recv(1024).decode()
        print("Recebido:")
        # printa mesagem recebida
        print(message)
        
        # tranforma string recebida em um vetor para a plotagem
        bit_array = []
        plot_data  = list(''.join(message))
        for bit in plot_data:
                if bit == '+':
                    bit_array.append(1)
                elif bit == '-':
                    bit_array.append(-1)
                else:
                    bit_array.append(0)
        
        # verifica se existe uma janela de gráfico aberta e fecha se existir
        if plt.fignum_exists(True):
            plt.close()

        # plota o gráfico da mensagem codificada recebida
        plt.rcParams["figure.autolayout"] = True
        plt.title('Recebido')
        index = list(np.arange(len(bit_array)))
        plt.bar(index, bit_array)        
        plt.show()

        # printa mesagem decodada
        print(decode(message))
        
        # pega nova mesagem do input e envia para o cliente
        data = input()
        data = encode(data)
        print(data)
        conn.send(data[0].encode()) 

        if plt.fignum_exists(True):
            plt.close()

        # plota o gráfico da mensagem codificada
        plt.rcParams["figure.autolayout"] = True
        plt.title('Enviado')
        index = list(np.arange(len(data[1])))
        plt.bar(index, data[1])        
        plt.show()

    conn.close() 