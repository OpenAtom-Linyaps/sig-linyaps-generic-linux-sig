## 编译构建指南

### 目标玲珑编译版本: 1.9.1-1 

在当前目录运行 ./build-rpm.sh 会自动下载源码并构建。
```
./build-rpm.sh
```

注意：此 shell 将会默认删除 ~/rpmbuild。可自行查阅调整和修改。

如果需要保留 ~/rpmbuild/BUILD 文件，请在脚本的构建命令中添加 --noclean 参数，如：
```
rpmbuild -bb linglong.spec --noclean
```