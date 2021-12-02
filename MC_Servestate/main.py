import OlivOS
import MC_Servestate.serve_base
import re
import json
import os
import threading
import time;
platform_bot_info = {}
listen_player_list = []

class Event(object):
    def init(plugin_event, Proc):
        bot_dict = Proc.Proc_data['bot_info_dict']
        for key,value in bot_dict.items():
            if value.platform["platform"] == "dodo":
                platform_bot_info["dodo"] = value
            elif value.platform["platform"] == "qq":
                platform_bot_info["qq"] = value
        return

    def private_message(plugin_event, Proc):
        pass

    def group_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)

    def save(plugin_event, Proc):
        pass


class Player:
    def __init__(self, name, ts):
        self.begin_time = ts
        self.name = name
        return

class Serve:
    def __init__(self, name, host ,port):
        self.name = name
        self.host = host
        self.port = int(port)
        return

class Process:
    def __init__(self):
        self.serve_list = []
        with open(data_file + "/serve_list.json",'r',encoding='utf8')as f:
            self.serve_data = json.load(f)
            for i in self.serve_data:
                serve_obj = Serve(i["name"],i["host"],i["port"])
                self.serve_list.append(serve_obj)
        return
    def get_player(self, serve_obj):
        #获取玩家数量和玩家列表的基本方法
        server = MC_Servestate.serve_base.StatusPing(serve_obj.host, serve_obj.port)
        json_data = server.get_status()
        if json_data == None:
            return -1, []
        player_list = []
        player_amount = json_data["players"]["online"]
        if "sample" in json_data["players"]:
            player_sample = json_data["players"]["sample"]
            for i in player_sample:
                player_list.append(i["name"])
        return player_amount, player_list

    def save_data(self, host, port, name):
        #储存当前内存中的数据
        self.serve_list.append(Serve(name, host, port))
        self.serve_data.append({"name":name,"host":host,"port":port})
        with open(data_file + "/serve_list.json",'w',encoding='utf8') as f:
            json.dump(self.serve_data, f)
        return

    def del_data(self, num):
        #删除对应的数据
        if num > len(self.serve_list):
            return False
        serve_obj = self.serve_list[num]
        self.serve_list.pop(num)
        self.serve_data.pop(num)
        with open(data_file + "/serve_list.json",'w',encoding='utf8') as f:
            json.dump(self.serve_data, f)
        return serve_obj

    def get_player_list(self):
        serve_str = []
        for i in range(0, len(self.serve_list)):
            player_amount, player_list = self.get_player(self.serve_list[i])
            if player_amount == -1:
                serve_str.append("[" + str(i) + "]" + self.serve_list[i].name + " : " + "服务器状态异常！")
            else:
                serve_str.append("[" + str(i) + "]" + self.serve_list[i].name + " : " + str(player_amount) + "人在线")
        return "\n".join(serve_str)

    def player_detail(self, num):
        num = int(num)
        if num > len(self.serve_list):
            return "该服务器并不存在！"
        player_amount, player_list = self.get_player(self.serve_list[num])
        if player_amount == 1:
            return "未知，原因：\n服务器状态异常！"
        return "\n".join(player_list)

    def listen_player(self):
        #监听玩家列表
        now_listen_list = []
        for i in range(0, len(self.serve_list)):
            if i > len(listen_player_list):
                #如果是新的id，则新建一个字典
                listen_player_list[i] = {}
            player_amount, player_list = self.get_player(self.serve_list[i])
            now_listen_list[i] = player_list
            #比对新旧列表
            old_player_list = listen_player_list[i]
            listen_player_list[i] = []
            for player in player_list:
                if i in old_player_list:
                    old_player_list.remove(player)
                    continue
                else:
                    ts = time.time()
                    #记录开始游玩时间
                    listen_player_list[i][player] = Player(player, ts)

            
        return

class LoopTimer(threading.Timer):
    def __init__(self, interval, function, args=[], kwargs={}):
        threading.Timer.__init__(self, interval, function, args, kwargs)
    def run(self):
        while True:
            self.finished.wait(self.interval)
            if self.finished.is_set():
                self.finished.set()
                break
            self.function(*self.args, **self.kwargs)

def listen_loop():
    bot_info = platform_bot_info["dodo"]
    plugin_event_fake = OlivOS.API.Event(OlivOS.contentAPI.fake_sdk_event(bot_info))
    plugin_event_fake.send('group', 131690, "测试", 108193)
    return

if __name__ != "__main__":
    data_file = "./plugin/data/MC_Servestate"
    if not os.path.exists(data_file):
        os.mkdir(data_file)
    if not os.access(data_file + "/serve_list.json", os.F_OK):
        f = open(data_file + "/serve_list.json","w",encoding='utf8')
        f.write("[]")
        f.close()
    process_obj = Process()
    t = LoopTimer(30, listen_loop)
    t.start()

def unity_reply(plugin_event, Proc):
    if plugin_event.data.message.startswith(('.', '。')):
        # 清除空格和首位
        message = plugin_event.data.message[1:].strip()
    else:
        return
    mat_set = re.search("mcset\s*([^\:]+)\:(\d{1,5})\s*(.+)", message, flags=re.I|re.M)
    mat_get = re.search("mcserve", message, flags=re.I|re.M)
    mat_det = re.search("mcplayer\s*(\d+)", message, flags=re.I|re.M)
    mat_del = re.search("mcdel\s*(\d+)", message, flags=re.I|re.M)
    if  mat_set:
        serve_host = mat_set.group(1)
        serve_port = mat_set.group(2)
        serve_name = mat_set.group(3)
        process_obj.save_data(serve_host, serve_port, serve_name)
        plugin_event.reply("添加成功√\n已将%s添加到列表中。" % (serve_name))
    if mat_get:
        plugin_event.reply("服务器状况如下：\n" + process_obj.get_player_list())
    if mat_det:
        plugin_event.reply("当前在线玩家：\n" + process_obj.player_detail(mat_det.group(1)))
    if mat_del:
        num = mat_del.group(1)
        serve_obj = process_obj.del_data(num)
        if serve_obj:
            plugin_event.reply("成功删除[%d](%s)服务器！" % num,serve_obj.name)
        else:
            plugin_event.reply("删除失败！原因：错误的序号。")
    
    return





