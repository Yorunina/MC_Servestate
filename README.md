# MC_Servestate
 Based On Ovo，a plugin to show the baisc state of minecraft server.

#### 前置：

**[	OlivOS](https://github.com/Yorunina/OlivOS)、Python 3.5+**

#### 面向平台：

 	**QQ、DoDo**

#### 功能概述：

​	通过socket建立握手关系，获取对应JE Minecraft服务器内人数、用户、描述、以及MOD

等信息的插件。

#### 参考档案：

​	[Server List Ping - wiki.vg](https://wiki.vg/Server_List_Ping)

------

#### 使用说明：

|               关键词                |                          描述                          |                   样例                    |
| :---------------------------------: | :----------------------------------------------------: | :---------------------------------------: |
| .mcset [服务器ip:端口] [服务器名称] |                 设置查询的mc服务器列表                 | .mcset dmcloud.mxmc.me:2002 Sky Factory 4 |
|              .mcserve               | 查询所有在列表中的服务器人数，同时返回服务器对应的[ID] |                                           |
|           .mcplayer [ID]            |                通过ID查询服务器玩家列表                |                .mcplayer 1                |

