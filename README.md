# QoS
基于SDN的QoS差异化服务系统

简介：
这是一款基于python的Django框架开发的web应用，用来实现对SDN网络进行流量管控，对指定的流量进行限速。
具体的功能模块包括：

1.登陆和注册

2.拓扑管理模块：可视化显示SDN网络topo信息

3.流表管理模块：在前端以列表形式显示ovs交换机中存在的流表信息、提供表单供用户输入参数下发新的流表项、
对交换机中存在的流表项进行删除

4.METER表管理模块：在前端显示ovs交换机中的meter表信息、提供表单供用户输入参数添加或删除meter表项

代码运行：

1.安装Django、mysql数据库、opendaylight carbon控制器、Mininet网络仿真工具、openvswitch交换机

2.首先使用mininet和opendaylight搭建SDN网络环境

3.在QoS文件夹下执行命令python manage.py runserver 0.0.0.0:8080，打开浏览器输入127.0.0.1:8080访问前
端页面



