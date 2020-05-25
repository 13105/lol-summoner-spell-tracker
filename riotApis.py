import sys, utils
import urllib.parse

class riotApis:

        
        
    
        
   
    def getSummonerByName(self, name):
        
        
        
        jsonUrl = "{}/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(
            self.urlBase,
            urllib.parse.quote(name.encode()),
            self.api_key
        )
        print("Pesquisando pelo nick \"{}\"...".format(name))
        ret = utils.getJson(jsonUrl)
        
        
        if ret == 403:
            print("Erro 403: chave de API invalida.")
            return ret
        
        if ret == 404:
            print("Erro 404: Invocador não existe.")
            return ret
        
        
        
        
        return ret
            
    def getEnemiesInfo(self, summonerId):
     
        jsonUrl = "{}/lol/spectator/v4/active-games/by-summoner/{}?api_key={}".format(
            self.urlBase,
            urllib.parse.quote(summonerId),
            self.api_key
        )
        
        
        print("Pesquisando pelo jogo atual do invocador \"{}\"...".format(summonerId))
        
        ret = utils.getJson(jsonUrl)
        
            
        if ret == 404:
            print("Erro: o invocador não está em partida (a partida terminou ?)")
            return ret
            
        players = ret["participants"]
        
        #[spell1, spell2, champion id, [runas]]
        playersInfo = []
        
        for player in players:
            if player["summonerId"] == summonerId:
                timeAliado = player["teamId"]
                break
        
        for player in players:
            if player["teamId"] == timeAliado:
                continue
            
            playersInfo.append([
            
                player["spell1Id"],
                player["spell2Id"],
                player["championId"],
                player["perks"]["perkIds"]
            
            ])
        
        
        return playersInfo
    def __init__(self, apiKey, regiao):
        
        self.api_key = apiKey
        regioes = {
            "BR1":  "br1.api.riotgames.com",
            "EUN1": "eun1.api.riotgames.com",
            "EUW1": "euw1.api.riotgames.com",
            "JP1": 	"jp1.api.riotgames.com",
            "KR": 	"kr.api.riotgames.com",
            "LA1": 	"la1.api.riotgames.com",
            "LA2": 	"la2.api.riotgames.com",
            "NA1": 	"na1.api.riotgames.com",
            "OC1": 	"oc1.api.riotgames.com",
            "TR1": 	"tr1.api.riotgames.com",
            "RU": 	"ru.api.riotgames.com" 
        }
        self.urlBase = "https://" + regioes[regiao]
        
        
 
