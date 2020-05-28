from tkinter import *
from tkinter import ttk
from tracker import TrackerWindow
from threading import Thread
import os.path
from riotApis import riotApis
from ddragon import DDragon
from urllib import request
from pathlib import Path
import time
class DownloadWindow(Frame):

    def call_inputWindow(self, ldata):

        #passa a intancia do arquivo já aberto para a proxima janela
        self.destroy()
        inputWindow = InputWindow(self.root_window, ldata)
    def getResources(self):


       ddragon = DDragon(
           realm="br",
           str_status1 = self.str_status1,
           str_status2 = self.str_status2,
           barra_status = self.barra_status,
           call_after_end = self.call_inputWindow
       )

       tGetResources = Thread(target=ddragon.getResources)
       tGetResources.start()
    def __init__(self, root_window):
        Frame.__init__(self, root_window)
        self.root_window = root_window

        COR_DE_FUNDO = "#FBFBFB"

        self.root_window.resizable(0, 0)
        self.root_window.title("Downloading resources...")

        self.root_window.config(
            bg=COR_DE_FUNDO
        )

        self.str_status1 = StringVar(self)




        self.config(
            bg=COR_DE_FUNDO
        )


        lbl_status1 = Label(
            self,
            text="-",
            bg=COR_DE_FUNDO,
            textvariable=self.str_status1
        )


        lbl_status1.pack(
            pady=(10, 10),

        )




        self.barra_status = ttk.Progressbar(
            self,
            orient="horizontal",
            length=300,
            mode="determinate"
        )
        self.barra_status.pack(
            padx=30
        )



        self.str_status2 = StringVar(self)

        lbl_status2 = Label(

            self,
            text="-",
            bg=COR_DE_FUNDO,
            textvariable=self.str_status2

        )



        lbl_status2.pack(
            pady=(10, 10),

        )


        root_window.after_idle(self.getResources)

        self.pack()



class InputWindow(Frame):

    #------- Funções ainda não usadas -------------
    def getSummonerIcon(self, icon_id):


        #icone já foi baixado ?
        if os.path.isfile(os.path.join(self.PF_ICONS_DIR, str(icon_id) + ".png")):
            print("ja foi baixado...")
            return


        #não, baixa-o
        arq_nome = str(icon_id) + ".png"
        url_icone = self.PF_ICONE_URL + arq_nome


        request.urlretrieve(
            url_icone,
            os.path.join(self.PF_ICONS_DIR, arq_nome)
        )
    #self.getSummonerIcon(player["profileIconId"])
    #----------------------------------------------

    def search_game_loop(self, player_id, riot_api, nick):
        #marca botão para a possibilidade de desativar

        self.btnSearch.config(
                bg=self.BTN_OFF_COR,
                text="Stop"
            )

        self.txtNick.config(
                state="disabled"
            )

        self.txtKey.config(
                state="disabled"
            )

        self.optRegiao.config(
                state="disabled"
            )

        while self.SEARCHING:
            enemies = riot_api.getEnemiesInfo(player_id)

            if enemies == 404:
                for i in range(20, 0, -1):
                    if self.SEARCHING:
                        self.status_msg("No active game found. Retrying in {}s".format(i))
                        time.sleep(1)
                    else:
                        self.str_src_status.set("")
                        break

                continue


            top = Toplevel()
            tracker = TrackerWindow(top, self.tracker_window_position, self.callback_STWP)

            tracker.start(enemies)

            self.status_msg("{}'s game found !".format(nick))

            #para loop
            self.SEARCHING = False





        #o loop foi parado, volta tudo ao estado normal
        self.btnSearch.config(
                    bg=self.BTN_ON_COR,
                    text="Start"
                )

        self.txtNick.config(
                    state="normal"
                )

        self.txtKey.config(
                    state="normal"
                )

        self.optRegiao.config(
                    state="normal"
                )

    def status_msg(self, msg):
        self.lbl_src_status.config(fg="#000")
        self.str_src_status.set(msg)

    def src_err_status(self, msg):
        self.lbl_src_status.config(fg="#F00")
        self.str_src_status.set(msg)

    def callback_STWP(self, pos):
        #SET TRACKER WINDOW POSITION, USADO PELO TRACKER
        self.tracker_window_position = pos
        return
    def btn_search_click(self):


        if not self.SEARCHING:

            nick = self.txtNick.get()
            key = self.txtKey.get()
            regiao = self.var_regiao.get()

            #valida entradas
            if len(nick) < 3 or len(nick) > 16:
                self.lbl_src_status.config(fg="#000")
                self.src_err_status("Error: Invalid summoner name.")
                return

            if len(key) < 1:
                self.lbl_src_status.config(fg="#F00")
                self.src_err_status("Error: API Key not specified.")
                return

            #dados validos !
            #apagar o arquivo e escrever nele as ultimas entradas usadas

            dados = [nick, regiao, key, self.tracker_window_position]
            with open("LDATA", "w") as arq:
                for d in dados:
                    arq.write(d + "\n")




            self.status_msg("Searching for the user...")


            apis = riotApis(key, regiao)
            player = apis.getSummonerByName(nick)

            if player == 403:
                self.src_err_status("Error 403: Invalid API Key.")
                return

            if player == 404:
                self.src_err_status("Error 404: Summoner does not exists.")
                return

            self.status_msg("Summoner found !")

            #começa a verificar se entrou em uma partida

            self.SEARCHING = True
            tSearching = Thread(target=self.search_game_loop, args=(player["id"], apis, nick))
            tSearching.start()

        else:
            self.SEARCHING = False



    def close_window(self):
        self.root_window.quit()




    def getLastConfigs(self, arq):
        ret = arq.read()
        return ret.splitlines()
    def LabelInput(self, container, texto):
        lblInput = Label(
            container,
            text=texto,
            font = ("Georgia", 10),
            bg = self.COR_DE_FUNDO
        )
        return lblInput
    def TextInput(self, container, largura, align="left"):

        txtInput = Entry(
            container,
            bd=2,
            relief=FLAT,
            highlightthickness=1,
            highlightbackground="#A9A9A9",
            width=largura,
            font=("consolas", 9, "bold"),
            justify=align,
            disabledforeground="#464646"
        )


        return txtInput
    def __init__(self, root_window, ldata=False):
        Frame.__init__(self, root_window)

        self.root_window = root_window
        self.root_window.title("Search current summoner's game")
        #self.root_window.geometry("650x200")
        self.COR_DE_FUNDO = "#FAFAFA"

        self.root_window.resizable(0, 0)
        self.root_window.protocol("WM_DELETE_WINDOW", self.close_window)


        self.root_window.iconbitmap("mya.ico")

        #FLAGS
        self.SEARCHING = False
        self.CLOSE_REQUEST = False
        self.CLOSE_OK = False


        self.BTN_OFF_COR = "#FF4A4A"
        self.BTN_ON_COR = "#5eba7d"

        #PF_ICONS -> PROFILE ICONS
        self.DATA_DIR = Path("data")
        self.PF_ICONS_DIR = os.path.join(self.DATA_DIR, "PF_ICONS")


        self.config(bg=self.COR_DE_FUNDO)
        container = LabelFrame(self, text="Query parameters", padx=30, pady=5, bg=self.COR_DE_FUNDO)


        lblNick = self.LabelInput(container, "Summoner's name:")

        self.txtNick = self.TextInput(container, 34, "center")


        regioes = [
            "BR1",
            "EUN1",
            "EUW1",
            "JP1",
            "KR",
            "LA1",
            "LA2",
            "NA1",
            "OC1",
            "TR1",
            "RU"
        ]

        self.var_regiao = StringVar(container)


        self.optRegiao = OptionMenu(
            container,
            self.var_regiao,
            *regioes
        )

        self.var_regiao.set(regioes[0])


        self.optRegiao.config(
            bd=0,
            relief=FLAT,
            highlightthickness=1,
            fg="#fff",
            highlightbackground="#A9A9A9",
            indicatoron=False,
            bg="#731595",
            font=("Helvetica", 8, "bold"),
            activeforeground="#731595",
            activebackground="#fff",
            padx=12,
            width=7
        )




        lblKey = self.LabelInput(container, "Riot API Key:")


        self.txtKey = self.TextInput(container, 40)
        self.txtKey.config(
            font=("Helvetica", 8),

        )

        self.btnSearch = Button(container, text="Search", command=self.btn_search_click)
        self.btnSearch.config(
            bd=0,
            relief=FLAT,
            fg="#fff",
            bg=self.BTN_ON_COR,
            font=("Helvetica", 10),
            width=8,
            activeforeground="#5eba7d",
            activebackground="#000",
            highlightcolor="#0f0"

        )


        self.str_src_status = StringVar(container)


        self.lbl_src_status = Label(
            self,
            font = ("Consolas", 11),
            textvariable=self.str_src_status,
            padx=30,
            bg = self.COR_DE_FUNDO
        )

        self.tracker_window_position = "+100+100"

        #posiciona widgets


        lblNick.grid(column=0, row=0, pady=(10,15))
        self.txtNick.grid(column=1, row=0, padx=(30, 20), pady=(10,15))
        self.optRegiao.grid(column=2, row=0, pady=(10,15))

        lblKey.grid(column=0, row=1, pady=(0, 20))
        self.txtKey.grid(column=1, row=1, padx=(30, 20), pady=(0, 20))
        self.btnSearch.grid(column=2, row=1, pady=(0, 20))


        container.pack(padx=35, pady=(10,15))
        self.lbl_src_status.pack(pady=(0,20))

        #ldata -> instancia para o arquivo das ultimas sessões

        if not ldata:
            #Não recebeu a instancia do arquivo da outra janela, logo esta não é a primeira vez
            with open("LDATA", "r") as arq:
                lastconfigs = self.getLastConfigs(arq)


            #dados anteriores foram preenchidos ?
            if len(lastconfigs) >= 3:
                self.txtNick.insert(0, lastconfigs[0])
                self.var_regiao.set(lastconfigs[1])
                self.txtKey.insert(0, lastconfigs[2])

                #a ultima posição do tracker foi salvada ?
                if len(lastconfigs) > 3:
                    self.tracker_window_position = lastconfigs[3]

        #pega URL da CDN no arquivo DDRAGON

        with open("DDRAGON", "r") as arq:
            self.CDN_URL = arq.read()

        self.PF_ICONE_URL = self.CDN_URL + "/img/profileicon/"


        self.pack()


def main():

    root = Tk()




    #verifica se é a primeira vez executando procurando pelo arquivo LDATA
    if not os.path.isfile("LDATA"):

        downloadWindow = DownloadWindow(root)

    else:
        inputW = InputWindow(root)


    root.mainloop()
if __name__ == "__main__":
    main()
