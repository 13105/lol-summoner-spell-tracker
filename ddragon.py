from pathlib import Path
from urllib import request
import utils, os.path, sys
import time
class DDragon:





    def getCDN_URL(self):
        #consulta apenas para pegar a versão atual da cdn
        print("Obtendo URL da CDN...")
        self.barra["maximum"] = 1
        self.barra["value"] = 0
        self.status1.set("Consultando URL da CDN...")


        json_arq = self.realm + ".json"

        self.status2.set(json_arq)

        jsonUrl = "https://ddragon.leagueoflegends.com/realms/" + json_arq
        dados = utils.getJson(jsonUrl)
        self.barra["value"] = 1

        #BUGADO
        #return dados["cdn"] + "/" + dados["dd"]

        return dados["cdn"] + "/10.10.3208608"
    def getSummonerSpells(self):

        self.barra["value"] = 0
        print("Obtendo informações sobre os feitiços de invocador...")
        self.status1.set("Obtendo informações sobre os feitiços de invocador...")
        self.status2.set("summoner.json")

        jsonUrl = self.CDN_URL + "/data/en_US/summoner.json"



        #verifica se a pasta existe, caso não, crie-a
        if not os.path.exists(self.ss_iconsDir):
            os.mkdir(self.ss_iconsDir)


        dados = utils.getJson(jsonUrl)

        self.barra["value"] = 1


        #Arquivo onde guarda cdrs das summoners spells
        ssArq = open(os.path.join(self.o_dir, "SS_CDR"), "w")
        ssIconeUrl = self.CDN_URL + "/img/spell/"
        spells = dados["data"]




        self.status1.set("Baixando icones dos feitiços de invocador...")
        self.barra["value"] = 0
        self.barra["maximum"] = len(dados["data"])

        time.sleep(5)
        for spellNome in dados["data"]:

            #Pega apenas id da spell, nome da imagem e cooldown
            spell = spells[spellNome]

            print("Baixando icones dos feitiços de invocador", spell["name"],"...")
            self.status2.set(spell["name"])




            ssArq.write(
                spell["key"] + "=" + spell["cooldownBurn"] + "\n"
            )



            request.urlretrieve(
                ssIconeUrl + spell["image"]["full"],
                os.path.join(self.ss_iconsDir, spell["key"] + ".png")
            )

            self.barra["value"] += 1
        ssArq.close()

    def getChampions(self):
        print("Obtendo informações dos campeões...")
        self.status1.set("Obtendo informações sobre os campões...")

        self.barra["maximum"] = 0
        self.barra["value"] = 0
        jsonUrl = self.CDN_URL + "/data/en_US/champion.json"

        self.status2.set("champion.json")

        dados = utils.getJson(jsonUrl)
        self.barra["value"] = 1
        return dados

    def getChampionsIcons(self, dados):



        #verifica se a pasta existe, caso não, crie-a
        if not os.path.exists(self.ch_iconsDir):
            os.mkdir(self.ch_iconsDir)


        chIconeUrl = self.CDN_URL + "/img/champion/"
        champions = dados["data"]


        self.barra["value"] = 0
        self.barra["maximum"] = len(dados["data"])

        self.status1.set("Baixando icones dos campeões...")
        for champ in champions:
            champion = champions[champ]


            print("Baixando o icone do campeão", champion["id"],"...")
            self.status2.set(champion["id"])

            request.urlretrieve(
                chIconeUrl + champion["image"]["full"],
                os.path.join(self.ch_iconsDir, champion["key"] + ".png")
            )
            self.barra["value"] +=1

    def getItemsIcons(self):
        self.barra["value"] = 0
        self.status1.set("Baixando icones de itens especificos...")
        if not os.path.exists(self.it_iconsDir):
            os.mkdir(self.it_iconsDir)

        self.barra["maximum"] = len(self.SS_CDR_ITEMS)
        url_icone_bota = self.CDN_URL + "/img/item/"
        for id in self.SS_CDR_ITEMS:
            arq_nome = (str(id) + ".png")
            self.status2.set(arq_nome)

            request.urlretrieve(
                    url_icone_bota + arq_nome,
                    os.path.join(self.it_iconsDir, arq_nome)
                )

            self.barra["value"] += 1

    def getChampions_R_Icons(self, dados):
        self.barra["value"] = 0
        self.status1.set("Baixando icones das ultimates...")
        print("Baixando icones das ultimates...")
        if not os.path.exists(self.r_icons):
            os.mkdir(self.r_icons)



    def getResources(self):
        self.CDN_URL = self.getCDN_URL()
        champions_dados = self.getChampions()
        self.getChampions_R_Icons(champions_dados)


        spells = self.getSummonerSpells()
        self.getChampionsIcons(champions_dados)

        self.getItemsIcons()




        #cria pasta para icones de invocador
        if not os.path.exists(self.pf_iconsDir):
            os.mkdir(self.pf_iconsDir)

        #cria arquivo para guardar o URL da CDN
        with open("DDRAGON", "w") as arq:
            arq.write(self.CDN_URL)

        #cria LDATA para guardar dados da ultima sessão
        with open("LDATA", "x"): pass
        self.call_after_end(True)


    def __init__(self, str_status1, str_status2, barra_status, call_after_end, realm = "na", o_dir = "data"):


        self.realm = realm
        self.o_dir = Path(o_dir)
        self.call_after_end = call_after_end

        if not os.path.exists(self.o_dir):
            os.mkdir(self.o_dir)

        #summoner spells icon dir
        self.ss_iconsDir = os.path.join(o_dir, "SS_ICONS")

        #champion icons dir
        self.ch_iconsDir = os.path.join(o_dir, "CH_ICONS")

        #profile icons dir
        self.pf_iconsDir = os.path.join(o_dir, "PF_ICONS")

        #items icons dir
        self.it_iconsDir = os.path.join(o_dir, "IT_ICONS")

        self.r_icons = os.path.join(o_dir, "R_ICONS")

        self.SS_CDR_ITEMS = [
            3158
        ]


        self.status1 = str_status1
        self.status2 = str_status2

        self.barra = barra_status


#if __name__ == "__main__":

    #ddragon = DDragon("br")
    #ddragon.getResources()
