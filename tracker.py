
from tkinter import *
from PIL import Image, ImageTk
from riotApis import riotApis
import os.path
from pathlib import Path
import time




class TrackerWindow(Frame):



    def rastrear_cdrs(self):

        tempo_atual = int(time.time())


        for p_id, player in enumerate(self.SS_TIMER_FLAGS):
            for SS in range(0,2):

                #contando ?
                if player[SS][0]:
                    if player[SS][1] <= tempo_atual:
                        # chegou a 0, para de contar
                        player[SS][0] = False

                        #esconde retangulo negro
                        player[SS][2].tag_raise(1)

                    tempo_restante = player[SS][1] - tempo_atual
                    player[SS][2].itemconfig(3, text=tempo_restante)


        self.root_window.after(200, self.rastrear_cdrs)
    def SS_CALLBACK_CLICK(self, e, segs, player_id, spellPos):
        # [icone, ofuscador do icone, texto]

        #manda icone para a ultima camada



        #CONTANDO ?
        if self.SS_TIMER_FLAGS[player_id][spellPos][0]:

            #sim, para de contar

            e.widget.tag_raise(1)
            self.SS_TIMER_FLAGS[player_id][spellPos][0] = False

        else:
            # não, começa a contar


            #marca quando vai recarregar
            self.SS_TIMER_FLAGS[player_id][spellPos][1] = int(time.time()) + segs

            e.widget.tag_lower(1)
            self.SS_TIMER_FLAGS[player_id][spellPos][0] = True


    def getSS_CDRS(self, spellsIds):

        arq = open(os.path.join(self.DATA_DIR, "SS_CDR"), "r")
        linhas = arq.read().splitlines()

        spellsCDR = {}
        for linha in linhas:
            id_cdr = linha.split("=")
            for id in spellsIds:


                #id encontrado
                if id == int(id_cdr[0]):
                    spellsCDR[id] = id_cdr[1]
                    spellsIds.remove(id)

            if len(spellsIds) < 1:
                break

        return spellsCDR


    def on_drop_rect(self, e):

        e.widget.itemconfig(self.rect_janela_txt, text="Saved !")

        janela_rect_coords = e.widget.coords(self.rect_janela)
        janela_rect_coords = list(map(lambda x: int(x), janela_rect_coords))



        #destroy canvas
        e.widget.destroy()
        self.container.pack()

        self.root_window.geometry(
            "%dx%d+%d+%d"%(
                self.janela_rect_w,
                self.janela_rect_h,
                janela_rect_coords[0],
                janela_rect_coords[1]
            )
        )

        #salva posição da janela para usar depois;
        with open("LDATA" ,"r") as arq:
            linhas = arq.read().splitlines()

        window_pos = "+%d+%d"%(janela_rect_coords[0], janela_rect_coords[1])

        with open("LDATA" ,"w") as arq:

            for i in range(0, 3):
                arq.write(linhas[i]+"\n")

            arq.write(window_pos + "\n")



        self.callback_STWP(window_pos)
    def on_drag_rect(self, e):


        janela_rect_coords = e.widget.coords(self.rect_janela)
        janela_txt_coords = e.widget.coords(self.rect_janela_txt)

        _x = janela_rect_coords[0]
        _y = janela_rect_coords[1]




        e.widget.itemconfig(self.rect_janela_txt, text="Release to drop")


        if (e.x > 0) and (_x <= self.SCREEN_W):
            e.widget.move(
                self.rect_janela,
                #novas cordenadas + meio do retangulo
                (-janela_rect_coords[0] + e.x) - (self.janela_rect_w / 2),
                0
            )


            #texto
            e.widget.move(
                self.rect_janela_txt,
                (-janela_txt_coords[0] + e.x),
                0
            )


        if (e.y > 0) and (_y <= self.SCREEN_H):

            e.widget.move(
                self.rect_janela,
                0,
                (-janela_rect_coords[1] + e.y) - (self.janela_rect_h / 3)
            )

            #texto
            e.widget.move(
                self.rect_janela_txt,
                0,
                (-janela_txt_coords[1] + e.y) + 10
            )


    def on_change_position_click(self):



        self.container.pack_forget()

        self.root_window.geometry(
            "%dx%d+%d+%d"%(self.SCREEN_W, self.SCREEN_H, 0, 0)
        )

        canvasFundo = Canvas(
                self,
                bg=self.TRANSPARENTE,
                bd=0,
                highlightthickness=0,
                width=self.SCREEN_W,
                height=self.SCREEN_H

        )
        self.janela_rect_w = self.container.winfo_width()
        self.janela_rect_h = self.container.winfo_height()




        canvasFundo.pack()


        self.rect_janela = canvasFundo.create_rectangle(0,0,self.janela_rect_w, self.janela_rect_h, fill="#fff")
        canvasFundo.move(
            self.rect_janela,
            (self.SCREEN_W/2) - (self.janela_rect_w/2),
            (self.SCREEN_H/2) - (self.janela_rect_h/2)
        )


        self.rect_janela_txt = canvasFundo.create_text(
            self.janela_rect_w/2,
            self.janela_rect_h/2,
            text="Hold to drag",
            font=("Georgia", 16, "bold")
        )

        canvasFundo.move(
            self.rect_janela_txt,
            (self.SCREEN_W/2) - (self.janela_rect_w/2),
            (self.SCREEN_H/2) - (self.janela_rect_h/2)
        )

        canvasFundo.tag_bind(self.rect_janela, "<B1-Motion>", self.on_drag_rect )
        canvasFundo.tag_bind(self.rect_janela_txt, "<B1-Motion>", self.on_drag_rect )

        canvasFundo.tag_bind(self.rect_janela, "<ButtonRelease-1>", self.on_drop_rect )
        canvasFundo.tag_bind(self.rect_janela_txt, "<ButtonRelease-1>", self.on_drop_rect )






    def start(self, enemies):
        #enemies -> lista de ints, contendo dados de players do time adversario


        ssIcones = {}
        chIcones = {}

        #Summoners spells usadas no time inimigo
        ssIds = []

        for arr in enemies:

            #verifica se a imagem da spell ou do champ já foi alocada

            #arr[0] e arr[1] == spell1 e spell2
            for i in range(0,2):
                if arr[i] not in ssIcones:
                    #referencia para spell ainda não alocada
                    ssIcones[arr[i]] = Image.open(os.path.join(self.SS_ICONS, str(arr[i])+".png" ))
                    ssIcones[arr[i]] = ssIcones[arr[i]].resize((self.SS_ICONE_SIZE_W, self.SS_ICONE_SIZE_H), Image.ANTIALIAS)
                    ssIds.append(arr[i])

            #arr[2] == icone do champ
            if arr[2] not in chIcones:
                #referencia para icone não alocada ainda
                chIcones[arr[2]] = Image.open(os.path.join(self.CH_ICONS, str(arr[2])+".png" ))
                chIcones[arr[2]] = chIcones[arr[2]].resize((self.CH_ICONE_SIZE_W, self.CH_ICONE_SIZE_H), Image.ANTIALIAS)




        #Tempo de recarga padrão de cada spell usada pelos players do time inimigo
        ssCDRS = self.getSS_CDRS(ssIds)







        #blocos para guardar referencias para 3 icones
        self.blocos = []


        #cor do retangulo que ofusca icone quando em recarga
        filamento = self.root_window.winfo_rgb(self.SS_ICONE_TRANSPARENTE_COR) + (self.SS_ICONE_TRANSPARENTE_OPACIDADE,)


        retangulo = Image.new(
            'RGBA',
            (self.SS_ICONE_SIZE_W, self.SS_ICONE_SIZE_H),
            filamento
        )

        self.RetanguloTransparente = ImageTk.PhotoImage(retangulo)


        #mini icone da bota
        bota_icone = Image.open(os.path.join(self.IT_ICONS, "3158.png" ))
        bota_icone = bota_icone.resize(
            (
                round(self.CH_ICONE_SIZE_W / 2),
                round(self.CH_ICONE_SIZE_H / 2)
            ),
            Image.ANTIALIAS

        )
        self.bota_icone = ImageTk.PhotoImage(bota_icone)

        #mini botão de fechar
        btnClose = Button(
            self.container,
            text="X",
            bg="#f00",
            fg="#FFF",
            font=("consolas", 7, "bold"),
            compound="center",
            width=2,
            height=0,
            bd=0,
            relief=FLAT,
            command=self.root_window.destroy
        )



        btnClose.grid(
            column=len(enemies),
            row=0,
            sticky="n"
        )


        #mini botão para mos

        btnChangeWindowPostion = Button(
            self.container,
            text="D",
            fg="#FFF",
            bg="#726FFF",
            font=("consolas", 8, "bold"),
            width=2,
            compound="center",
            height=0,
            bd=0,
            relief=FLAT,
            command=self.on_change_position_click
        )



        btnChangeWindowPostion.grid(
            column=len(enemies),
            row=0,
            sticky="s"
        )



        #para cada player, monta o conteudo da janela

        for i, arr in enumerate(enemies):

            self.blocos.append(
                [
                ImageTk.PhotoImage(chIcones[arr[2] ]),
                ImageTk.PhotoImage(ssIcones[arr[0] ]),
                ImageTk.PhotoImage(ssIcones[arr[1] ]),
                ]
            )


            #retrato do champ
            ch_retrato = Canvas(
                self.container,
                bg="#000",
                bd=0,
                width=self.CH_ICONE_SIZE_W,
                height=self.CH_ICONE_SIZE_H,
                highlightthickness=0
            )






            #Canvas para icones
            canvasSS1 = Canvas(
                self.container,
                width=self.SS_ICONE_SIZE_W,
                height=self.SS_ICONE_SIZE_H ,
                bd=0,
                highlightthickness=0,
                relief='ridge',
                bg=self.TRANSPARENTE,
                cursor=self.SS_HOVER_CURSOR,

            )

            canvasSS2 = Canvas(
                self.container,
                width=self.SS_ICONE_SIZE_W,
                height=self.SS_ICONE_SIZE_H ,
                bd=0,
                highlightthickness=0,
                relief='ridge',
                bg=self.TRANSPARENTE,
                cursor=self.SS_HOVER_CURSOR

            )


            #TODO: POSICIONAR O ICONE DA BOTA DE UM MODO EM QUE O ICONE DO CAMPEÃO FIQUE MAIS VISIVEL
            #TODO: CRIAR UMA BORDA AO REDOR DO ICONE DA BOTA PARA ESCONDER A AREA PRETA

            retrato = ch_retrato.create_image(
                0,
                0,
                image=self.blocos[i][0],
                anchor="nw"
            )

            #ICONE DE BOTA:

            #retrato = ch_retrato.create_image(
            #    self.SS_CDR_ITEM_ICONE_X,
            #    self.SS_CDR_ITEM_ICONE_Y,
            #    image=self.bota_icone,
            #    anchor="nw"
            #)

            #cria imagem dos summoners spells
            ss1_id = canvasSS1.create_image(
                0,
                0,
                image=self.blocos[i][1],
                anchor='nw'
            )

            ss2_id = canvasSS2.create_image(
                0,
                0,
                image=self.blocos[i][2],
                anchor='nw'
            )




            #cria imagem do retangulo negro para ofuscar os icones
            canvasSS1.create_image(
                0,
                0,
                image=self.RetanguloTransparente,
                anchor='nw'
            )

            canvasSS2.create_image(
                0,
                0,
                image=self.RetanguloTransparente,
                anchor='nw'
            )


            #verifica se o player esta usando a runa de reduzir cdr
            spell1CDR = int(ssCDRS[arr[0]])
            spell2CDR = int(ssCDRS[arr[1]])


            if self.SS_RUNA_REDUCAO in arr[3]:
                spell1CDR = round(spell1CDR - ((spell1CDR * 5) / 100))
                spell2CDR = round(spell2CDR - ((spell2CDR * 5) / 100))






            #cria texto para contagem de cdr no meio do icone

            canvasSS1.create_text(
                self.SS_TEXT_POSITION_X,
                self.SS_TEXT_POSITION_Y,
                fill=self.SS_FONT_COLOR,
                font=("Consolas", self.SS_FONT_SIZE, "bold"),
                anchor="nw"

            )

            canvasSS2.create_text(
                self.SS_TEXT_POSITION_X,
                self.SS_TEXT_POSITION_Y,
                fill=self.SS_FONT_COLOR,
                font=("Consolas", self.SS_FONT_SIZE, "bold"),
                anchor="nw"

            )


            canvasSS1.tag_raise(ss1_id)
            canvasSS2.tag_raise(ss2_id)


            ch_retrato.grid(
                    column=i,
                    row=0,
                    padx=round(self.CH_ICONE_SIZE_W / 10)
            )

            canvasSS1.grid(
                column=i,
                row=1,
                sticky=W,
                padx=(
                    round(self.CH_ICONE_SIZE_W / 10),
                    0
                ),
                pady=(1,0)
            )


            canvasSS2.grid(
                column=i,
                row=1,
                sticky=E,
                padx=(
                    0,
                    round(self.CH_ICONE_SIZE_W / 10)
                ),
                pady=(1,0)
            )







            self.SS_TIMER_FLAGS.append(
                [
                    #FlagContando, QuandoRecarrega, widget
                    [False, 0, canvasSS1],
                    [False, 0, canvasSS2]
                ]
            )


            canvasSS1.bind("<Button-1>", lambda e, arg=spell1CDR, arg2=i: self.SS_CALLBACK_CLICK(e, arg, arg2, 0 ) )
            canvasSS2.bind("<Button-1>", lambda e, arg=spell2CDR, arg2=i: self.SS_CALLBACK_CLICK(e, arg, arg2, 1 ) )

        self.container.pack()
        self.pack()

        self.rastrear_cdrs()



    def __init__(self, root_window, window_position, callback_STWP):
        Frame.__init__(self, root_window)


        #Constantes da janela
        self.root_window = root_window
        self.root_window.geometry(window_position)

        self.TRANSPARENTE = "#F0F"
        self.SS_HOVER_CURSOR = "hand2"


        #PROPORÇÃO DO CONTEUDO DA JANELA
        self.PROPORCAO_CONTEUDO = 36

        #Tamanho do icone do champ e detalhes dos summoners spells
        self.CH_ICONE_SIZE_W = self.PROPORCAO_CONTEUDO
        self.CH_ICONE_SIZE_H = self.PROPORCAO_CONTEUDO

        self.SS_ICONE_SIZE_W = round(self.PROPORCAO_CONTEUDO / 2)
        self.SS_ICONE_SIZE_H = round(self.PROPORCAO_CONTEUDO / 2)


        self.SS_FONT_SIZE = round((self.SS_ICONE_SIZE_W / 10) * 3.9)

        self.SS_TEXT_POSITION_X = round(self.SS_ICONE_SIZE_W / 10)
        self.SS_TEXT_POSITION_Y = round((self.SS_ICONE_SIZE_H / 10) * 1.6 )

        self.SS_CDR_ITEM_ICONE_X = round(self.CH_ICONE_SIZE_W / 2)
        self.SS_CDR_ITEM_ICONE_Y = round(self.CH_ICONE_SIZE_H / 2)

        self.SS_ICONE_TRANSPARENTE_OPACIDADE = round(0.7 * 255)
        self.SS_ICONE_TRANSPARENTE_COR = "#000"

        self.SS_FONT_COLOR = "#FFF"


        #ID da runa que reduz cdr por 5%
        self.SS_RUNA_REDUCAO = 8347

        #Flags do estado de cada timer
        self.SS_TIMER_FLAGS = []


        #Diretorios
        self.DATA_DIR = Path("data")
        self.CH_ICONS = os.path.join(self.DATA_DIR, "CH_ICONS")
        self.SS_ICONS = os.path.join(self.DATA_DIR, "SS_ICONS")
        self.IT_ICONS = os.path.join(self.DATA_DIR, "IT_ICONS")



        #seta detalhes da janela
        self.root_window.resizable(0, 0)
        self.root_window.wm_attributes("-topmost", True)
        self.root_window.wm_attributes("-transparentcolor", self.TRANSPARENTE)
        self.root_window.overrideredirect(1)
        self.root_window.configure(bg=self.TRANSPARENTE)


        self.container = Frame(self, bg=self.TRANSPARENTE)
        self.SCREEN_W = 1360
        self.SCREEN_H = 768

        self.JANELA_W = self.container.winfo_width()
        self.JANELA_H = self.container.winfo_height()







        self.callback_STWP = callback_STWP

        self.config(
            bg=self.TRANSPARENTE
        )






#enemies = [
#[14, 4, 53, [8439, 8446, 8429, 8242, 8347, 8321, 5008, 5008, 5002]],
#[4, 14, 82, [8010, 9111, 9105, 8014, 8139, 8135, 5008, 5008, 5003]],
#[7, 4, 21, [8005, 9101, 9103, 8014, 8304, 8345, 5005, 5008, 5002]],
#[12, 4, 80, [9923, 8126, 8138, 8105, 9105, 8014, 5008, 5008, 5002]],
#[14, 11, 35, [8112, 8143, 8138, 8105, 8233, 8236, 5005, 5008, 5002]]
#]

#root = Tk()
#tracker = TrackerWindow(root,"+100+100", NONE)
#tracker.start(enemies)
#root.mainloop();
