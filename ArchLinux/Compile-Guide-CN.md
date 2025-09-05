# Arch Linux (pacman 系编译指导)

### 软件包状态

- linyaps 

[![Packaging status](https://repology.org/badge/vertical-allrepos/linyaps.svg)](https://repology.org/project/linyaps/versions)

- linyaps-box

[![Packaging status](https://repology.org/badge/vertical-allrepos/linyaps-box.svg)](https://repology.org/project/linyaps-box/versions)

- linyaps-web-store-installer 

[![Packaging status](https://repology.org/badge/vertical-allrepos/linyaps-web-store-installer.svg)](https://repology.org/project/linyaps-web-store-installer/versions)

- linglong-pica

[![Packaging status](https://repology.org/badge/vertical-allrepos/linglong-pica.svg)](https://repology.org/project/linglong-pica/versions)

- linglong-tools

[![Packaging status](https://repology.org/badge/vertical-allrepos/linglong-tools.svg)](https://repology.org/project/linglong-tools/versions)

## 在线安装

### 安装 linyaps 发行版

通过 [Arch Linux extra 仓库](https://archlinux.org/packages/extra/x86_64/linyaps/) 安装 linyaps

```bash
sudo pacman -Syu linyaps
```

### 安装 linyaps-git 开发版

通过 [AUR](https://aur.archlinux.org/packages/linyaps-git) 或[自建源](https://github.com/taotieren/aur-repo) 安装 linyaps-git

```bash
yay -Syu linyaps-git
```

### 安装 linyaps-box 发行版

通过 [Arch Linux extra 仓库](https://archlinux.org/packages/extra/x86_64/linyaps-box/) 安装 linyaps-box

```bash
sudo pacman -Syu linyaps-box
```

### 安装 linyaps-box-git 开发版

通过 [AUR](https://aur.archlinux.org/packages/linyaps-box-git) 或[自建源](https://github.com/taotieren/aur-repo) 安装 linyaps-box-git

```bash
yay -Syu linyaps-box-git
```

### 安装 linyaps-web-store-installer 发行版

通过 [AUR](https://aur.archlinux.org/packages/linyaps-web-store-installer) 或[自建源](https://github.com/taotieren/aur-repo) 安装 linyaps-web-store-installer

```bash
yay -Syu linyaps-web-store-installer
```

### 安装 linyaps-web-store-installer-git 开发版

通过 [AUR](https://aur.archlinux.org/packages/linyaps-web-store-installer-git) 或[自建源](https://github.com/taotieren/aur-repo) 安装 linyaps-web-store-installer

```bash
yay -Syu linyaps-web-store-installer-git
```

### 安装 linglong-pica 发行版

通过 [AUR](https://aur.archlinux.org/packages/linglong-pica) 或[自建源](https://github.com/taotieren/aur-repo) 安装 linglong-pica

```bash
yay -Syu linglong-pica
```

### 安装 linglong-pica-git 开发版

通过 [AUR](https://aur.archlinux.org/packages/linglong-pica-git) 或[自建源](https://github.com/taotieren/aur-repo) 安装 linglong-pica-git

```bash
yay -Syu linglong-pica-git
```

### 安装 linglong-tools 发行版

通过 [AUR](https://aur.archlinux.org/packages/linglong-tools) 或[自建源](https://github.com/taotieren/aur-repo) 安装 linglong-tools

```bash
yay -Syu linglong-tools
```

### 安装 linglong-tools-git 开发版

通过 [AUR](https://aur.archlinux.org/packages/linglong-tools-git) 或[自建源](https://github.com/taotieren/aur-repo) 安装 linglong-tool-git

```bash
yay -Syu linglong-tools-git
```

## 本地编译安装

### 安装 linyaps

```bash
#  克隆 ArchLinux 的 linyaps 软件包仓库
git clone https://gitlab.archlinux.org/archlinux/packaging/packages/linyaps.git
# 进入 linyaps 目录
cd linyaps
# 修改 PKGBUILD 中的版本号
vim PKGBUILD
# 更新校验值并本地编译
updpkgsums && makepkg -sf
# 安装 linyaps 
# 注意 -debug 是调试包，可选安装
sudo pacman -U linyaps*
```
### 安装 linyaps-box

```bash
#  克隆 ArchLinux 的 linyaps-box 软件包仓库
git clone https://gitlab.archlinux.org/archlinux/packaging/packages/linyaps-box.git
# 进入 linyaps-box 目录
cd linyaps-box
# 修改 PKGBUILD 中的版本号
vim PKGBUILD
# 更新校验值并本地编译
updpkgsums && makepkg -sf
# 安装 linyaps-box 
# 注意 -debug 是调试包，可选安装
sudo pacman -U linyaps-box*
```

### 安装 linyaps-web-store-installer

```bash
# 进入 linyaps-web-store-installer 目录
cd linyaps-web-store-installer
# 修改 PKGBUILD 中的版本号
vim PKGBUILD
# 更新校验值并本地编译
updpkgsums && makepkg -sf
# 安装 linyaps-web-store-installer
# 注意 -debug 是调试包，可选安装
sudo pacman -U linyaps-web-store-installer*
```

### 安装 linglong-pica

```bash
# 进入 linglong-pica 目录
cd linglong-pica
# 修改 PKGBUILD 中的版本号
vim PKGBUILD
# 更新校验值并本地编译
updpkgsums && makepkg -sf
# 安装 linglong-pica 
# 注意 -debug 是调试包，可选安装
sudo pacman -U linglong-pica*
```

### 安装 linglong-tools

```bash
# 进入 linglong-tools 目录
cd linglong-tools
# 修改 PKGBUILD 中的版本号
vim PKGBUILD
# 更新校验值并本地编译
updpkgsums && makepkg -sf
# 安装 linglong-tools 
# 注意 -debug 是调试包，可选安装
sudo pacman -U linglong-tools*
```

