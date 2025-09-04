# Fedora (RPM系编译指南)

## 目标玲珑编译版本:1.9.10 
#### 注意:不建议在docker/podman下进行编译,因为USER变量缺失,而且使用wget下载会大概率出问题,除非您有能力进行对应的更改

## 一.自动编译教程

下载仓库当前目录里的build-rpm.sh执行即可,执行后会在当前目录输出安装包

## 二.手动编译教程
## 目标玲珑-Pica编译版本:上游Master

#### 注意:

#### 1.不建议在docker下进行编译,因为USER变量缺失,而且使用wget下载会大概率出问题,除非您有能力进行对应的更改

#### 2.Fedora下无法转换DEB包为玲珑包,只能转换AppImage和Flatpak版

# 自动编译教程:

## (自动编译适用于代码编译无问题并希望及时跟随上游的场景)

#### 在一个干净的文件夹里直接执行:

#### `wget https://raw.githubusercontent.com/OpenAtom-Linyaps/sig-linyaps-generic-linux-sig/refs/heads/main/Fedora/linglong-pica/build-rpm.sh && bash build-rpm.sh`

### 如果没有编译问题就会在当前文件夹下生成RPM安装包 (编译环境也会同时清理掉)

# 手动编译教程:

## (手动编译情况适用于需要自行修改源码场景)

## 一.准备环境

### 1.安装RPM编译所需依赖:

#### `sudo dnf install @development-tools rpmdevtools rpmlint wget -y`

### 2.进入到对应用户的"~"文件夹,也就是

### `cd /home/${USER}`

#### 3.新建RPM包编译工作环境

#### `rpmdev-setuptree`

## 二.拷贝文件

### 1.进入工作编译目录

#### `cd /home/${USER}/rpmbuild`

### 2.在rpmbuild/SOURCES目录下载.zip格式的玲珑源代码

#### `cd SOURCES && wget -O linyaps.zip https://github.com/LFRon/linyaps-generic-linux/archive/refs/tags/1.9.9-1.zip && cd ..`

### 3.在rpmbuild/SPECS目录下载本仓库的spec文件

#### `cd SPECS && wget https://raw.githubusercontent.com/OpenAtom-Linyaps/sig-linyaps-generic-linux-sig/refs/heads/main/Fedora/linglong/linglong.spec && cd ..`

## 三.安装构建依赖

### 进入rpmbuild/SPECS目录后使用dnf命令安装对应依赖即可

#### `cd SPECS && sudo dnf builddep linglong.spec -y`

## 四.进行构建并生成RPM包

### `rpmbuild -bb linglong.spec`

#### 之后产生的RPM安装包就在`~/rpmbuild/RPMS/<对应架构>`下,将其全部导出并进行分发即可

