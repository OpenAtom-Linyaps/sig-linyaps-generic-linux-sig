#!/bin/bash

echo "- 请在下方输入您的当前用户密码"
sudo echo "- 提权成功!"
sleep 0.3
echo "- 开始编译"
sleep 0.5
clear

#先获取当前目录
current_dir=${PWD}

# 设置工作目录
WORKDIR="/home/${USER}/rpmbuild"

#更新软件源并安装编译所需的基础依赖
sudo dnf update && sudo dnf install @development-tools rpmdevtools rpmlint wget -y

#设置软件编译文件夹
rpmdev-setuptree

#进入编译工作目录
cd ${WORKDIR}

echo "- 正在下载源码"
#下载最新源码压缩包
cd SOURCES && wget -O linglong-pica.zip https://github.com/linuxdeepin/linglong-pica/archive/refs/heads/master.zip && cd ..

echo "- 正在下载SPEC编译文件"
#下载最新SPEC编译文件
cd SPECS && wget https://raw.githubusercontent.com/OpenAtom-Linyaps/sig-linyaps-generic-linux-sig/refs/heads/main/Fedora/linglong-pica/linglong-pica.spec && cd ..

echo "- 正在安装编译依赖"
#进入SPEC文件所在文件夹并安装编译依赖
sudo dnf builddep ${WORKDIR}/SPECS/linglong-pica.spec -y

echo "- 开始编译"
#开始编译
rpmbuild -bb ${WORKDIR}/SPECS/linglong-pica.spec

echo "- 正在拷贝RPM安装包"
#拷贝RPM安装包到当前目录
cp ${WORKDIR}/SPECS/RPMS/*/* ${current_dir}

echo "- 清理编译目录"
#清理工作目录
sudo rm -r ${WORKDIR}/SPECS

echo "- 玲珑-Pica的RPM安装包构建完成!"
