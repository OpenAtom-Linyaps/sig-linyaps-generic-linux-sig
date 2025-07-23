# Fedora (RPM系编译指南)

## 目标玲珑编译版本:1.10.0-Alpha0 (使用日构建版原因:更新速度快)
## 目前自动编译功能暂时无法使用,需要手动编译

#### 注意:不建议在docker下进行编译,因为USER变量缺失,而且使用wget下载会大概率出问题,除非您有能力进行对应的更改

## 一.自动编译教程

下载仓库当前目录里的build-rpm.sh执行即可,执行后会在当前目录输出安装包

## 二.手动编译教程

## 1.构建玲珑-box (目标玲珑-box版本:2.0)

### 1.安装RPM编译所需依赖:

`sudo dnf install @development-tools rpmdevtools rpmlint wget -y`

### 2.进入到对应用户的"~"文件夹,也就是

`cd ~`

### 3.新建RPM包编译工作环境

`rpmdev-setuptree`

### 4.进入rpmbuild目录,并在rpmbuild/SOURCES目录下载.zip格式的玲珑-box的源代码

`cd rpmbuild/SOURCES && wget -O linyaps-box.zip https://github.com/deepin-community/linyaps-box/archive/refs/heads/release/2.0.zip && cd ..`

### 5.在rpmbuild/SPECS目录下载本仓库的spec文件

`cd SPECS && wget https://raw.githubusercontent.com/OpenAtom-Linyaps/sig-linyaps-generic-linux-sig/refs/heads/main/Fedora/linglong-box/linglong-box.spec && cd ..`

### 6.进入rpmbuild/SPECS目录后使用dnf命令安装对应依赖即可

`cd SPECS && sudo dnf builddep linglong-box.spec -y`

### 7.进行构建并生成RPM包

`rpmbuild -bb linglong-box.spec`



### 之后产生的玲珑-box的RPM安装包就在`~/rpmbuild/RPMS/<对应架构>`下,将其全部导出并进行分发即可



### 注意:如果要继续构建玲珑本体,记得输入`cd ~ && rm -r rpmbuild`清理构建目录!



## 2.构建玲珑本体

### 1.安装RPM编译所需依赖:

`sudo dnf install @development-tools rpmdevtools rpmlint wget -y`

### 2.进入到对应用户的"~"文件夹,也就是

`cd /home/${USER}`

### 3.新建RPM包编译工作环境

`rpmdev-setuptree`

## 二.拷贝文件

### 1.进入工作编译目录

`cd ~/rpmbuild`

### 2.在rpmbuild/SOURCES目录下载.zip格式的玲珑的源代码

`cd SOURCES && wget -O linyaps.zip https://gitee.com/LFRon/Linyaps-generic-linux-SIG/releases/download/1.9.4-1/linyaps-1.9.4-1-source.zip && cd ..`

### 3.在rpmbuild/SPECS目录下载本仓库的spec文件

`cd SPECS && wget https://raw.githubusercontent.com/OpenAtom-Linyaps/sig-linyaps-generic-linux-sig/refs/heads/main/Fedora/linglong/linglong.spec && cd ..`

## 三.安装构建玲珑

### 进入rpmbuild/SPECS目录后使用dnf命令安装对应依赖即可

`cd SPECS && sudo dnf builddep linglong.spec -y`

## 四.进行构建并生成RPM包

`rpmbuild -bb linglong.spec`

#### 之后产生的RPM安装包就在`~/rpmbuild/RPMS/<对应架构>`下,将其全部导出并进行分发即可
