from urllib import request
import urllib.error
from urllib.request import urlopen
import json

def getJson(jsonUrl):
    req = request.Request(jsonUrl)
    
    try:
        ret = urlopen(req)
        if(ret.getcode() == 200):
            return json.load(ret)
  
    
        
    except urllib.error.HTTPError as http_err:
        return http_err.code
        
    except Exception as e:
        raise e