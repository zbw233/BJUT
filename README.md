# README

## Setup Instructions

配置gem5-gpu过程

第一步，下载gem5-gpu
从http://gem5-gpu.cs.wisc.edu网站下载gem5-gpu
网站使用mercurial版本管理，并且下载需要使用特殊的qclone命令，所以需要修改/etc/mercurial/hgrc文件添加
[extensions]
mq=
保存后即可使用qclone
1）创建一个路径
      mkdir gem5-gpu
      cd gem5-gpu
2）下载gem5并给gem5打patches
      hg qclone http://repo.gem5.org/gem5 -p http://gem5-gpu.cs.wisc.edu/repo/gem5-patches
      cd gem5/
      hg update -r <gem5-revision>
      hg qpush -a
      cd ../
3）下载gpgpu-sim并打patch
      hg qclone http://gem5-gpu.cs.wisc.edu/repo/gpgpu-sim -p http://gem5-gpu.cs.wisc.edu/repo/    gpgpu-sim-patches
      cd gpgpu-sim
      hg qpush -a
      cd ../
4）下载gem5-gpu glue 代码
      hg clone http://gem5-gpu.cs.wisc.edu/repo/gem5-gpu

第二步，安装所有gem5-gpu依赖项
1）修改/etc/apt/sources.list的内容为:

      deb http://mirrors.aliyun.com/ubuntu/ wily main restricted universe multiverse
      deb http://mirrors.aliyun.com/ubuntu/ wily-security main restricted universe multiverse
      deb http://mirrors.aliyun.com/ubuntu/ wily-updates main restricted universe multiverse
      deb http://mirrors.aliyun.com/ubuntu/ wily-proposed main restricted universe multiverse
      deb http://mirrors.aliyun.com/ubuntu/ wily-backports main restricted universe multiverse

      deb-src http://mirrors.aliyun.com/ubuntu/ wily main restricted universe multiverse
      deb-src http://mirrors.aliyun.com/ubuntu/ wily-security main restricted universe multiverse
      deb-src http://mirrors.aliyun.com/ubuntu/ wily-updates main restricted universe multiverse
      deb-src http://mirrors.aliyun.com/ubuntu/ wily-proposed main restricted universe multiverse
      deb-src http://mirrors.aliyun.com/ubuntu/ wily-backports main restricted universe multiverse

2）联网进行源的更新，执行以下命令以便获取和安装运行gem5所需软件包。 

      sudo apt-get update && sudo apt-get dist-upgrade

3）执行以下命令，安装运行gem5模拟器及gem5_utils工具所需的软件包。
      
      sudo apt-get install git mercurial scons build-essential vim geany swig zlib1g-dev libgoogle-perftools-dev protobuf-compiler libprotobuf-dev m4 python-dev python3-pip python3-lxml python3-pydot python3-matplotlib python3-pandas python3-seaborn
 
4）修改PyPI(Python Package Index, Python包索引)镜像，将~/.pip/pip.conf的内容修改为：

      [global]
      index-url = https://pypi.mirrors.ustc.edu.cn/simple

5）执行以下命令，安装运行gem5_utils工具所需的Python3软件包。

      pip3 install objectpath yattag pytz

执行以下命令，以从mcai的github项目网站下载最新版本的gem5_utils实用工具源码。

      cd gem5-gpu
      git clone https://github.com/mcai/gem5_utils.git --verbose


4）安装cuda与cuda sdk
      安装cuda版本推荐为3.1或3.2，gem5-gpu只能运行在这两个版本上，其他版本编译会出现问题
      在https://developer.nvidia.com/cuda-toolkit-32-downloads下载并安装cuda toolkits3.2与cuda SDK
5）设置环境变量
      export CUDAHOME=cuda根目录
第三步 编译gem5-gpu
       
       cd gem5
       scons build/X86_VI_hammer_GPU/gem5.opt --default=X86 EXTRAS=../gem5-gpu/src:../gpgpu-sim/ PROTOCOL=VI_hammer GPGPU_SIM=True
 
       编译成功

第四步 下载benchmark并编译

1） 下载
       cd gem5-gpu
       hg clone https://gem5-gpu.cs.wisc.edu/repo/benchmarks/
2） 编译
       1.编译需要使用gcc与g++ 4.4版本
	gcc更换版本命令如下
	apt-get install gcc-4.4 g++-4.4
        cd /usr/bin
	ln -s gcc-4.4 gcc
	ln -s g++-4.4 g++
       2.更换gcc版本后编译libcuda
	[gem5-gpu/benchmarks] cd libcuda
        [gem5-gpu/benchmarks/libcuda] make
       3.编译所有benchmarks
	cd gem5-gpu/benchmarks/rodinia
	./buildall.sh

## TODOs

1. Clone lru.cc and lru.hh as bypass.cc and hh, Put GPU data in LRU position; put CPU data in MRU position.
2. Integrate GPUWattch.
3. thesis.
