#!/bin/bash

#先获取当前目录
current_dir=${PWD}

#进入主目录
cd ~

#更新软件源并安装编译所需的基础依赖
sudo dnf update && sudo dnf install @development-tools rpmdevtools rpmlint wget -y

#设置软件编译文件夹
rpmdev-setuptree

#进入编译工作目录
cd ~/rpmbuild

echo "- 正在下载源码"
#下载最新源码压缩包
cd SOURCES && wget -O linglong-pica.zip https://github.com/linuxdeepin/linglong-pica/archive/refs/heads/master.zip && cd ..

echo "- 正在下载SPEC编译文件"
#下载最新SPEC编译文件
cd SPECS && wget https://raw.githubusercontent.com/OpenAtom-Linyaps/sig-linyaps-generic-linux-sig/refs/heads/main/Fedora/linglong-pica/linglong-pica.spec && cd ..

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
