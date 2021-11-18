import MC_Servestate.serve_base
import re
import json
import os

class Event(object):
    def init(plugin_event, Proc):
        pass

    def private_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)

    def save(plugin_event, Proc):
        pass

class serve:
    def __init__(self):
        with open(data_file + "/serve_list.json",'r',encoding='utf8')as f:
            self.serve_list = json.load(f)
        return
    def get_player(self, host, port):
        server = MC_Servestate.serve_base.StatusPing(host, port)
        json_data = server.get_status()
        player_list = []
        player_amount = json_data["players"]["online"]
        if "sample" in json_data["players"]:
            player_sample = json_data["players"]["sample"]
            for i in player_sample:
                player_list.append(i["name"])
        return player_amount, player_list
    def save_data(self, host, port, name):
        self.serve_list.append({"host":host, "port":port, "name":name})
        with open(data_file + "/serve_list.json",'w',encoding='utf8')as f:
            json.dump(self.serve_list, f)
        return
    def get_player_list(self):
        serve_str = []
        for i in range(0, len(self.serve_list)):
            player_amount, player_list = self.get_player(self.serve_list[i]["host"], int(self.serve_list[i]["port"]))
            serve_str.append("[" + str(i) + "]" + self.serve_list[i]["name"] + " : " + str(player_amount) + "人在线")
        return "\n".join(serve_str)
    def player_detail(self, num):
        num = int(num)
        if num > len(self.serve_list):
            return "该服务器并不存在！"
        player_amount, player_list = self.get_player(self.serve_list[num]["host"], int(self.serve_list[num]["port"]))
        return "\n".join(player_list)

if __name__ != "__main__":
    data_file = "./plugin/data/MC_Servestate"
    if not os.path.exists(data_file):
        os.mkdir(data_file)
    if not os.access(data_file + "/serve_list.json", os.F_OK):
        f = open(data_file + "/serve_list.json","w",encoding='utf8')
        f.write("[]")
        f.close()
    serve_obj = serve()

def unity_reply(plugin_event, Proc):
    if plugin_event.data.message.startswith(('.', '。')):
        # 清除空格和首位
        message = plugin_event.data.message[1:].strip()
    else:
        return
    mat_set = re.search("mcset\s*([^\:]+)\:(\d{1,5})\s*(.+)", message, flags=re.I|re.M)
    mat_get = re.search("mcserve", message, flags=re.I|re.M)
    mat_det = re.search("mcplayer\s*(\d+)", message, flags=re.I|re.M)
    if  mat_set:
        serve_host = mat_set.group(1)
        serve_port = mat_set.group(2)
        serve_name = mat_set.group(3)
        serve_obj.save_data(serve_host, serve_port, serve_name)
        plugin_event.reply("添加成功√\n已将%s添加到列表中。"%(serve_name))
    if mat_get:
        plugin_event.reply("服务器状况如下：\n" + serve_obj.get_player_list())
    if mat_det:
        plugin_event.reply("当前在线玩家：\n" + serve_obj.player_detail(mat_det.group(1)))
    return





