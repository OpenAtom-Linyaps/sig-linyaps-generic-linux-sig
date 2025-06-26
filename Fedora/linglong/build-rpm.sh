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
rm -r rpmbuild

#更新软件源并安装编译所需的基础依赖
sudo dnf update && sudo dnf install @development-tools rpmdevtools rpmlint wget -y

#设置软件编译文件夹
rpmdev-setuptree

echo "- 正在下载源码"
#下载最新源码压缩包
wget -O ~/rpmbuild/SOURCES/linyaps.zip https://github.com/OpenAtom-Linyaps/linyaps/archive/refs/tags/1.9.1.zip

echo "- 正在安装编译依赖"
#安装编译依赖
sudo dnf builddep ./linglong.spec -y

echo "- 开始编译"
#开始编译
rpmbuild -bb ./linglong.spec 

echo "- 正在拷贝RPM安装包"
#拷贝RPM安装包到当前目录
cp ~/rpmbuild/RPMS/*/* ${current_dir}

echo "- 清理编译目录"
#清理工作目录
rm -r ~/rpmbuild

echo "- 玲珑本体RPM安装包构建完成!"
