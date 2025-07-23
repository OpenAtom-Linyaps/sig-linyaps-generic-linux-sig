# Fedora (RPM系编译指导)

## 目标linglong-web-store-installer编译版本:1.6.6-1



# 自动编译教程:

## (自动编译脚本还没写)





# 手动编译教程:

## (手动编译情况适用于需要自行修改源码场景)

## 一.准备环境

1.安装RPM编译所需依赖:

`sudo dnf install @development-tools rpmdevtools rpmlint wget -y`

2.进入到对应用户的"~"文件夹,也就是

`cd /home/${USER}`

3.新建RPM包编译工作环境

`rpmdev-setuptree`

## 二.拷贝文件

1.进入工作编译目录

`cd /home/${USER}/rpmbuild`

2.在rpmbuild/SOURCES目录下载.zip格式的玲珑源代码

`cd SOURCES && wget -O linyaps-web-store-installer.zip https://github.com/OpenAtom-Linyaps/linyaps-web-store-installer/archive/refs/tags/v1.6.6.zip && cd ..`

3.在rpmbuild/SPECS目录下载本仓库的spec文件

`cd SPECS && wget https://raw.githubusercontent.com/OpenAtom-Linyaps/sig-linyaps-generic-linux-sig/refs/heads/main/Fedora/linglong-web-store-installer/linyaps-web-store-installer.spec && cd ..`

## 三.安装构建依赖

进入rpmbuild/SPECS目录后使用dnf命令安装对应依赖即可

`cd SPECS && sudo dnf builddep linyaps-web-store-installer.spec -y`

## 四.进行构建并生成RPM包

`rpmbuild -bb linglong.spec`

#### 之后产生的RPM安装包就在`~/rpmbuild/RPMS/<对应架构>`下,将其全部导出并进行分发即可
