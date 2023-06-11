import tkinter as tk
from client import *
class Interface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('8B6T Client')
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.geometry('205x160')
        self.window.minsize(205, 160)
        self.window.maxsize(205, 160)

        self.create_connection_toggle = tk.BooleanVar()
        self.local_connection_toggle = tk.BooleanVar()
        self.host = tk.StringVar()
        self.port = tk.StringVar()

        # instancia o cliente
        self.client = Client()

        # cria frame de conexao e widgets
        self.connect_frame = tk.Frame(self.window)
        self.host_entry = tk.Entry(self.connect_frame)
        self.local_connection_checkbutton = tk.Checkbutton(self.connect_frame)

        # cria frame de mensagem e widgets
        self.message_frame = tk.Frame(self.window)
        self.history_text = tk.Text(self.message_frame)
        self.message_text = tk.Text(self.message_frame)

        self.history_index = 0.0
        self.init_connection_frame()

        self.receive_toggle = tk.BooleanVar()
        self.receive_toggle.set(False)

        self.window.mainloop()

    def init_connection_frame(self):
        tk.Label(self.connect_frame, text="Conectar").grid(column=0, row=0, sticky=tk.W)

        tk.Checkbutton(self.connect_frame, text='Criar sessao', variable=self.create_connection_toggle, command=self.check_if_creating)\
            .grid(column=0, row=1, sticky=(tk.W, tk.E, tk.S, tk.N))

        self.local_connection_checkbutton.config(text="Conexao local", variable=self.local_connection_toggle, command=self.check_if_local)
        self.local_connection_checkbutton.grid(column=0, row=2, sticky=(tk.W, tk.E, tk.S, tk.N))

        tk.Label(self.connect_frame, text="Host").grid(column=0, row=3, sticky=(tk.W, tk.E))

        self.host_entry.configure(width=7, textvariable=self.host)
        self.host_entry.grid(column=1, row=3, sticky=(tk.W, tk.E, tk.S, tk.N))

        tk.Label(self.connect_frame, text="Port").grid(column=0, row=4, sticky=(tk.W, tk.E, tk.S, tk.N))

        tk.Entry(self.connect_frame, width=7, textvariable=self.port).grid(column=1, row=4, sticky=(tk.W, tk.E, tk.S, tk.N))

        tk.Button(self.connect_frame, command=self.connect, text='Conectar').grid(column=1, row=5, sticky=(tk.W, tk.E, tk.S, tk.N))

        self.connect_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.S, tk.N))

    def init_message_frame(self):
        scrollbar = tk.Scrollbar(self.message_frame, orient='vertical', command=self.history_text.yview)
        scrollbar.grid(column=2, row=0, sticky=(tk.W, tk.N, tk.S))

        self.history_text.config(height=20, width=100, yscrollcommand=scrollbar.set)
        self.history_text.grid(column=0, row=0, columnspan=2, sticky=(tk.W, tk.E))

        self.message_text.config(height=5, width=80)
        self.message_text.grid(column=0, row=1, rowspan=2, sticky=tk.W)

        tk.Button(self.message_frame, command=self.receive_message, text='Receber').grid(column=1, row=2, sticky=(tk.W, tk.E, tk.S, tk.N))

        send_button = tk.Button(self.message_frame, command=self.send_message, height=2, width=20, text='Enviar')
        send_button.grid(column=1, row=1, sticky=(tk.W, tk.E, tk.N))

        self.message_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.S, tk.N), padx=5, pady=5)

    def connect(self):
        try:
            self.client.host = self.host.get()
            self.client.port = int(self.port.get())
            if self.create_connection_toggle.get():
                self.client.create_connection()
                self.client.is_host = True
            else:
                self.client.connect()
            self.connect_frame.destroy()
            self.init_message_frame()
            self.window.geometry('758x450')
            self.window.minsize(758, 450)
            self.window.maxsize(758, 450)

        except TimeoutError:
            print("Nao foi possivel conectar a" + self.client.host + ":" + str(self.client.port))

    def check_if_local(self):
        if self.local_connection_toggle.get():
            self.host_entry.configure(state='disabled')
            self.host.set(get_ip())
        else:
            self.host_entry.configure(state='normal')
            self.host.set('')

    def check_if_receiving(self):
        if self.receive_toggle.get():
            self.receive_message()

    def check_if_creating(self):
        if self.create_connection_toggle.get():
            self.local_connection_checkbutton.config(state='disabled')
            self.host_entry.configure(state='disabled')
            self.host.set(get_ip())
            print('LOCAL: ', get_ip())
        else:
            self.local_connection_checkbutton.config(state='normal')
            self.host_entry.configure(state='normal')
            self.host.set('')

    def send_message(self):
        message = self.message_text.get('0.0', tk.END)

        message = message.removesuffix('\n')

        self.client.set_message_to_send(message)

        # pega as variaveis do client e armazena no tk.Text de historico
        self.history_text.insert(tk.END, 'ENVIADO:\n')

        self.history_text.insert(tk.END, '- Texto:\n')

        self.history_text.insert(tk.END, self.client.text_message)
        self.history_text.insert(tk.END, '\n\n')

        self.history_text.insert(tk.END, '- Encriptado:\n')

        self.history_text.insert(tk.END, self.client.caesar)
        self.history_text.insert(tk.END, '\n\n')

        self.history_text.insert(tk.END, '- ASCII:\n')

        self.history_text.insert(tk.END, self.client.ascii_message)
        self.history_text.insert(tk.END, '\n\n')

        self.history_text.insert(tk.END, '- Binario:\n')

        self.history_text.insert(tk.END, self.client.binary_message)
        self.history_text.insert(tk.END, '\n\n')

        self.history_text.insert(tk.END, '- Codificado:\n')

        self.history_text.insert(tk.END, self.client.encoded_message)
        self.history_text.insert(tk.END, '\n\n\n\n')

        self.window.update()
        self.client.send_message()
        self.receive_toggle.set(True)

        self.message_text.delete('0.0', tk.END)

    def receive_message(self):
        self.client.receive_message()

        # pega as variaveis do client e armazena no tk.Text de historico
        self.history_text.insert(tk.END, 'RECEBIDO:\n')

        self.history_text.insert(tk.END, '- Codificado:\n')

        self.history_text.insert(tk.END, self.client.encoded_message)
        self.history_text.insert(tk.END, '\n\n')

        self.history_text.insert(tk.END, '- Binario:\n')

        self.history_text.insert(tk.END, self.client.binary_message)
        self.history_text.insert(tk.END, '\n\n')

        self.history_text.insert(tk.END, '- ASCII:\n')

        self.history_text.insert(tk.END, self.client.ascii_message)
        self.history_text.insert(tk.END, '\n\n')

        self.history_text.insert(tk.END, '- Encriptado:\n')

        self.history_text.insert(tk.END, self.client.caesar)
        self.history_text.insert(tk.END, '\n\n')

        self.history_text.insert(tk.END, '- Texto:\n')

        self.history_text.insert(tk.END, self.client.text_message)
        self.history_text.insert(tk.END, '\n\n\n\n')

        self.receive_toggle.set(False)
