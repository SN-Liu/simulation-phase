# simulation-phase
基于CarMaker仿真软件，读取所需信息并输出

将user.c lineds.c lineds.h makefile 四个文件，复制到项目文件夹的src文件夹中
利用msys进行编译
    1.cd到项目文件夹的src地址下
    2.make
打开carmaker，修改application configuration中command为 src/CarMaker.win64.exe
然后start&connect即可
使用如下命令行，以特定端口打开carmaker
C:\IPG\carmaker\win64-11.1.2\bin\CM.exe -cmdport 16660
打开simulation_phase
开始运行carmaker中的仿真程序以及python脚本-simulation_phase.py，即可从carmaker中读取信息
