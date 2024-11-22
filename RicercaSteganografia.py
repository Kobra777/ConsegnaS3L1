import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Toplevel, Text, Scrollbar
from stegano import lsb
from PIL import Image, ImageTk

# Inizializzazione della variabile globale a None
percorso_immagine = None

def seleziona_immagine():
    global percorso_immagine, immagine_visualizzata
    percorso_immagine = filedialog.askopenfilename()
    if not percorso_immagine:
        messagebox.showwarning("Attenzione", "Nessun file selezionato.")
        return
    try:
        img = Image.open(percorso_immagine)
        img.thumbnail((250, 250))
        immagine_visualizzata = ImageTk.PhotoImage(img)
        tela.create_image(125, 125, image=immagine_visualizzata)
        tela.grid()
    except IOError:
        messagebox.showerror("Errore", "Impossibile aprire il file selezionato.")
        percorso_immagine = None  # Resetta il percorso se l'immagine non è valida
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")
        percorso_immagine = None

def nascondi_messaggio():
    global percorso_immagine
    if percorso_immagine is None:
        messagebox.showwarning("Attenzione", "Prima devi caricare un'immagine.")
        return
    messaggio = simpledialog.askstring("Input", "Inserisci il messaggio segreto da nascondere:")
    if not messaggio:
        messagebox.showwarning("Attenzione", "Nessun messaggio inserito.")
        return
    try:
        segreta = lsb.hide(percorso_immagine, messaggio)
        percorso_salvataggio = filedialog.asksaveasfilename(defaultextension=".png")
        if percorso_salvataggio:
            segreta.save(percorso_salvataggio)
            messagebox.showinfo("Fatto", "Messaggio nascosto nell'immagine!")
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore durante il tentativo di nascondere il messaggio: {str(e)}")

def rivela_messaggio():
    global percorso_immagine
    if percorso_immagine is None:
        messagebox.showwarning("Attenzione", "Prima devi caricare un'immagine.")
        return
    try:
        messaggio_rivelato = lsb.reveal(percorso_immagine)
        messaggio = f"Messaggio nascosto: {messaggio_rivelato}" if messaggio_rivelato else "Nessun messaggio nascosto trovato."
        messagebox.showinfo("Messaggio Rivelato", messaggio)
    except Exception as e:
        messagebox.showerror("Errore", f"C'è un errore generico. Prova ad interpretarlo, dai non è complicato: {str(e)}")

def mostra_ricerca():
    top = Toplevel(app)
    top.title("Ricerca sulla Steganografia")
    scroll = Scrollbar(top)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    text = Text(top, wrap='word', font=('Helvetica', 12), yscrollcommand=scroll.set)
    scroll.config(command=text.yview)
    text.insert(tk.END, "Steganografia: Un'Arte Antica Rivisitata nell'Era Digitale\n\n"
                        "Storia e Tecniche Base\n"
                        "La steganografia è un'arte antica che consiste nel nascondere informazioni all'interno di altri messaggi o oggetti fisici. "
                        "Questa pratica ha origini che risalgono agli antichi Greci. "
                        "Originariamente, le tecniche impiegate includevano l'utilizzo di inchiostri invisibili e il celamento di messaggi in oggetti fisici, "
                        "come pezzi di seta. Nel corso dei secoli, è stata adottata per trasmettere comunicazioni segrete in ambiti militari e diplomatici.\n\n"
                        "Tecniche di Steganografia Digitale\n"
                        "Con l'evoluzione della tecnologia digitale, anche le tecniche di steganografia si sono evolute. "
                        "Ecco alcune delle principali forme:\n"
                        "- Steganografia di Testo: Impiega caratteri Unicode non stampabili, come lo Zero-Width Joiner e il Zero-Width Non-Joiner, "
                        "per nascondere informazioni all'interno di testi.\n"
                        "- Steganografia di Immagini: Si basa sulla modifica dei bit meno significativi dei pixel di un'immagine. "
                        "Questo permette di nascondere dati senza alterare visibilmente l'immagine.\n"
                        "- Steganografia Audio e Video: Consiste nell'incorporamento di dati segreti all'interno di file audio e video, "
                        "manipolando spesso i bit meno significativi per inserire messaggi.\n"
                        "- Steganografia in Reti di Comunicazione: Nasconde dati all'interno del traffico di rete, "
                        "utilizzando, ad esempio, i pacchetti TCP/IP o i parametri dei codec in flussi audio VoIP.\n\n"
                        "Considerazioni di Sicurezza e Steganalisi\n"
                        "Sebbene la steganografia fornisca un metodo efficace per celare dati, la steganalisi è la disciplina che si occupa di scoprire tali messaggi nascosti. "
                        "Con l'incremento dell'uso di tecniche sempre più sofisticate, anche la steganalisi ha visto un'evoluzione, "
                        "adottando algoritmi di machine learning per identificare anomalie nei file che potrebbero suggerire la presenza di dati occulti.\n"
                        "La steganografia rimane un campo estremamente affascinante che unisce segretezza e innovazione, "
                        "trovando applicazione tanto in contesti legittimi quanto in ambiti meno etici, come il malware e lo spionaggio informatico.")
    text.pack(expand=True, fill='both')
    top.geometry("800x600")

app = tk.Tk()
app.title("App di Steganografia")

tela = tk.Canvas(app, width=250, height=250)
btn_carica = tk.Button(app, text="Carica Immagine", command=seleziona_immagine)
btn_nascondi = tk.Button(app, text="Nascondi Messaggio", command=nascondi_messaggio)
btn_rivela = tk.Button(app, text="Rivela Messaggio", command=rivela_messaggio)
btn_mostra_ricerca = tk.Button(app, text="Mostra Ricerca", command=mostra_ricerca)

btn_carica.grid(row=0, column=0, sticky="ew")
btn_nascondi.grid(row=1, column=0, sticky="ew")
btn_rivela.grid(row=2, column=0, sticky="ew")
btn_mostra_ricerca.grid(row=3, column=0, sticky="ew")

app.mainloop()
