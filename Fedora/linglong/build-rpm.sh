#!/bin/bash

echo "- 请在下方输入您的当前用户密码"
sudo echo "- 提权成功!"
sleep 0.3
echo "- 开始编译"
sleep 0.5
clear
#先获取当前目录
current_dir=${PWD}

#进入主目录并清理可能有的旧rpmbuild安装包
cd ~ && rm -r rpmbuild

#更新软件源并安装编译所需的基础依赖
sudo dnf update && sudo dnf install @development-tools rpmdevtools rpmlint wget -y

#设置软件编译文件夹
rpmdev-setuptree

#进入编译工作目录
cd ~/rpmbuild

echo "- 正在下载源码"
#下载最新源码压缩包
cd SOURCES && wget -O linyaps.zip https://github.com/LFRon/linyaps-generic-linux/archive/refs/tags/1.9.9-1.zip && cd ..

echo "- 拷贝编译文件到SPECS"
cd SPECS && cp ${current_dir}/linglong.spec ./

echo "- 正在安装编译依赖"
#进入SPEC文件所在文件夹并安装编译依赖
cd SPECS && sudo dnf builddep linglong.spec -y

echo "- 开始编译"
#开始编译
rpmbuild -bb linglong.spec

echo "- 正在拷贝RPM安装包"
#拷贝RPM安装包到当前目录
cp ~/rpmbuild/RPMS/*/* ${current_dir}

echo "- 清理编译目录"
#清理工作目录
sudo rm -r ~/rpmbuild

echo "- 玲珑本体RPM安装包构建完成!"
