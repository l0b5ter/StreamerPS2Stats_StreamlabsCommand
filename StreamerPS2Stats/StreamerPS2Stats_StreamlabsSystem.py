#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
sys.platform = "win32"
import os, threading, json, codecs, traceback, time
import re
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import MySettings
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "StreamerPS2Stats"
Website = "https://github.com/l0b5ter/StreamerPS2Stats_StreamlabsCommand"
Description = "Show streamer's planetside2 stats"
Creator = "lobster/loster31345"
Version = "1.0.0.0"

#---------------------------
#   Define Global Variables
#---------------------------

global baseapi
global Factions 
global Command
baseapi = "https://census.daybreakgames.com/s:lobster/get/ps2:v2/"
Factions = ["nc", "tr", "vs"]
Command = "stats"

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():
    global CommandFileList
    directory = os.path.join(os.path.dirname(__file__), "Config")
    if not os.path.exists(directory):
        os.makedirs(directory)
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    if data.IsChatMessage() and data.GetParam(0).lower() == Command: 
        OnlinePlayer = ""
        for x in Factions:
            OnlineWho = PlayerLoopUp(x)
            if OnlineWho != "":
                OnlinePlayer = OnlineWho
        if OnlinePlayer != "":
            PlayerResponse = ApiResponse(OnlineWho)
            kphString = "\n KPM: " + GetPlayerKPH(PlayerResponse)
            kdrString = "\n KDR: " + GetPlayerKDR(PlayerResponse)
            adrString = "\n ADR: " + GetPlayerADR(PlayerResponse)
            scoString = "\n Score/Minute: " + GetPlayerScore(PlayerResponse)
            capString = "\n Total-captures: " + GetPlayerDefs(PlayerResponse)
            defString = "\n Total-defends: " + GetPlayerCaps(PlayerResponse)
            SendResp(data, "Showing stats for " + OnlinePlayer + kphString + kdrString + adrString + scoString + capString + defString)
            return
    return

def PlayerLoopUp(faction):
    status = ""
    CommandFile = os.path.join(os.path.dirname(__file__), 'Config/' + faction + '.json')
    CommandFileList = MySettings(CommandFile)
    OnlinePlayer = re.findall(r"[\w']+", CommandFileList.player)
    for i in OnlinePlayer:
        Playername = i.lower()
        Parent.Log(ScriptName, Playername)
        if GetOnlinePlayer(i) == "true":
            status = i
            return  status
    return status


def GetOnlinePlayer(playerlist):
    IsOnline = ""
    
    api = baseapi + "character/?name.first_lower=" + playerlist.lower() +"&c:join=characters_online_status&c:limit=5000"
    #Parent.SendStreamMessage(api)
    apidata = json.loads(Parent.GetRequest(api, {}))
    apiresponse = json.loads(apidata['response'])
    #Parent.Log(ScriptName, json.dumps(apiresponse))
    #Parent.Log(ScriptName, api)
    for character in apiresponse["character_list"]:
        Parent.Log(ScriptName, str(character["character_id_join_characters_online_status"]))
        if character["character_id_join_characters_online_status"]["online_status"] != "0":
            IsOnline = "true"
        else:
            IsOnline = "false"
    return IsOnline

def ApiResponse(charname):
    api = baseapi + "character/?name.first_lower=" + charname + "&c:resolve=stat_history&c:limit=5000"
    apidata = json.loads(Parent.GetRequest(api, {}))
    
    if apidata["status"] == 200:
        apiresponse = json.loads(apidata['response'])
    return apiresponse

def GetPlayerScore(apiresponse):
    score = float(apiresponse["character_list"][0]["stats"]["stat_history"][8]["all_time"])
    time = float(apiresponse["character_list"][0]["stats"]["stat_history"][9]["all_time"])

    return str(round(score/(time/60), 2))

def GetPlayerKDR(apiresponse):
    kills = float(apiresponse["character_list"][0]["stats"]["stat_history"][5]["all_time"])
    deaths = float(apiresponse["character_list"][0]["stats"]["stat_history"][2]["all_time"])
    #return str(kills)
    return str(round(kills/deaths,2))

def GetPlayerADR(apiresponse):        
    captures = float(apiresponse["character_list"][0]["stats"]["stat_history"][3]["all_time"])
    defends = float(apiresponse["character_list"][0]["stats"]["stat_history"][4]["all_time"])
    return str(round(captures/defends, 2))

def GetPlayerCaps(apiresponse):        
    captures = float(apiresponse["character_list"][0]["stats"]["stat_history"][3]["all_time"])
    return str(captures)

def GetPlayerDefs(apiresponse):        
    defends = float(apiresponse["character_list"][0]["stats"]["stat_history"][4]["all_time"])
    return str(defends)

def GetPlayerKPH(apiresponse):
    kills = float(apiresponse["character_list"][0]["stats"]["stat_history"][5]["all_time"])
    time = float(apiresponse["character_list"][0]["stats"]["stat_history"][9]["all_time"])

    return str(round(kills/(time/60), 2))


#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return


#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return



def SendResp(data, Message):

    if not data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendStreamMessage(Message)

    if not data.IsFromDiscord() and data.IsWhisper():
        Parent.SendStreamWhisper(data.User, Message)

    if data.IsFromDiscord() and not data.IsWhisper():
        Parent.SendDiscordMessage(Message)

    if data.IsFromDiscord() and data.IsWhisper():
        Parent.SendDiscordDM(data.User, Message)
    return