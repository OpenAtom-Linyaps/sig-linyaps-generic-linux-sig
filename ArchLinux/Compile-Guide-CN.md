# Arch Linux (pacman 系编译指导)

## 在线安装

### 安装 linyaps

通过 [AUR](https://aur.archlinux.org/packages/linyaps) 或[自建源](https://github.com/taotieren/aur-repo) 安装 linyaps

```bash
yay -Syu linyaps
```
### 安装 linglong-pica

通过 [AUR](https://aur.archlinux.org/packages/linglong-pica) 或[自建源](https://github.com/taotieren/aur-repo) 安装 linglong-pica

```bash
yay -Syu linglong-pica
```

## 本地编译安装

### 安装 linyaps

```bash
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

