from socket import * 
from threading import *
from tkinter import *
from tkinter import filedialog
from datetime import datetime

client = socket(AF_INET, SOCK_STREAM)

ip = "10.100.5.231"
port = 4444

client.connect((ip, port))

pencere = Tk()

pencere.title("Bağlandı: "+ ip +" "+ str(port))

message = Text(pencere, width=50)
message.grid(row =0, column=0, padx=10, pady=10,)

mesaj_giris = Entry(pencere, width=50)
mesaj_giris.insert(0, "Adınız *")

mesaj_giris.grid(row=1,column=0,
                 padx=10,pady=10,
                 )

mesaj_giris.focus()
mesaj_giris.selection_range(0, END)

def mesaj_gonder(event=None):
    istemci_mesaji = mesaj_giris.get()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message.insert(END, '\n' + 'Sen :'+ istemci_mesaji + ' ' + timestamp)
    client.send(istemci_mesaji.encode('utf8'))
    mesaj_giris.delete(0, END)

btn_msj_gonder = Button(pencere, text="Gönder", width=15, command=mesaj_gonder)
btn_msj_gonder.grid(row=2, column=0, pady=10,padx=10)

pencere.bind('<Return>', mesaj_gonder)

def gelen_msaj_kontrol():
    while True:
        server_msg = client.recv(1024).decode('utf8')
        message.insert(END, '\n'+ server_msg)

def dosya_ac():
    dosya_yolu = filedialog.askopenfilename()
    print(dosya_yolu)  

btn_dosya_ac = Button(pencere, text="Gözat", width=15, command=dosya_ac)
btn_dosya_ac.grid(row=2, column=1, pady=10,padx=10)

recv_kontrol = Thread(target=gelen_msaj_kontrol)
recv_kontrol.daemon = True
recv_kontrol.start()

pencere.mainloop()
