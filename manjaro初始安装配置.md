# 设置镜像源
配置中国的 mirrors，在终端执行下面的命令从官方的源列表中对中国源进行测速和设置：
```bash{.line-numbers}
sudo pacman-mirrors -c China -m rank
```
为 Manjaro 增加中文社区的源来加速安装软件，在 /etc/pacman.conf中添加archlinuxcn源，末尾加上：
```vim{.line-numbers}
[archlinuxcn]
SigLevel = Optional TrustedOnly
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```
安装 archlinux-keyring 包以导入 GPG key，否则的话 key 验证失败会无法安装：
```shell{.line-numbers}
sudo pacman -S archlinux-keyring
```
同步并更新系统：
```shell{.line-numbers}
sudo pacman -Syyu
```
# 中文输入法
fcitx 是 Free Chinese Input Toy for X 的缩写，国内也常称作小企鹅输入法，是一款 Linux 下的中文输入法:
```bash{.line-numbers}
sudo pacman -S fcitx-googlepinyin
sudo pacman -S fcitx-im # 选择全部安装
sudo pacman -S fcitx-configtool # 安装图形化配置工具
sudo pacman -S fcitx-skin-material
```
解决中文输入法无法切换问题: 添加文件 ~/.xprofile：
```vim{.line-numbers}
export GTK_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS="@im=fcitx"
```
输入法需要重启生效
# pacman常用命令
```shell{.line-numbers}
sudo pacman -S 软件名　# 安装
sudo pacman -R 软件名　# 删除单个软件包，保留其全部已经安装的依赖关系
sudo pacman -Rs 软件名 # 除指定软件包，及其所有没有被其他已安装软件包使用的依赖关系
sudo pacman -Ss 软件名  # 查找软件
sudo pacman -Sc # 清空并且下载新数据
sudo pacman -Syu　# 升级所有软件包
sudo pacman -Qs # 搜索已安装的包
```
# yay
Yay 是用 Go 编写的 Arch Linux AUR 包管理工具。具体可以查看 Arch Wiki
安装 yay：
```shell{.line-numbers}
sudo pacman -S yay
```
配置 yay 的 aur 源为清华源 AUR 镜像：
```shell{.line-numbers}
yay --aururl "https://aur.tuna.tsinghua.edu.cn" --save
```
修改的配置文件位于 ~/.config/yay/config.json ，还可通过以下命令查看修改过的配置:
```shell{.line-numbers}
yay -P -g
```
yay 的常用命令：
```shell{.line-numbers}
yay -S package # 从 AUR 安装软件包
yay -Rns package # 删除包
yay -Syu # 升级所有已安装的包
yay -Ps # 打印系统统计信息
yay -Qi package # 检查安装的版本
```
yay 安装命令不需要加 sudo。
# Git
```shell{.line-numbers}
git config --global user.name "Michael728"
git config --global user.email "649168982@qq.com"
ssh-keygen -t rst -C "649168982@qq.com"
```
# zsh
```shell{.line-numbers}
sudo pacman -S zsh # 安装zsh
echo $SHELL # 查看大概年前 shell
chsh -s /bin/zsh # 修改默认shell，这个是修改当前用户的终端，如果要修改 root 账户，需要切换到 root用户
wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh
sudo pacman -S autojump
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```
需要重启生效
# 终端代理
### 方法一
在终端中直接运行：
```shell{.line-numbers}
export http_proxy=http://proxyAddress:port
```
这个办法的好处是简单直接，并且影响面很小（只对当前终端有效，退出就不行了）。
如果你用的是ss代理，在当前终端运行以下命令，那么wget curl 这类网络命令都会经过ss代理
```shell{.line-numbers}
export ALL_PROXY=socks5://127.0.0.1:1080
```
### 方法二
把代理服务器地址写入shell配置文件.bashrc或者.zshrc
直接在.bashrc或者.zshrc添加下面内容
```vim{.line-numbers}
export http_proxy="http://localhost:port"
export https_proxy="http://localhost:port"
```
以使用shadowsocks代理为例，ss的代理端口为1080,那么应该设置为
```vim{.line-numbers}
export http_proxy="socks5://127.0.0.1:1080"
export https_proxy="socks5://127.0.0.1:1080"
```
或者直接设置ALL_PROXY
```vim{.line-numbers}
export ALL_PROXY=socks5://127.0.0.1:1080
```
localhost就是一个域名，域名默认指向 127.0.0.1，两者是一样的。
然后ESC后:wq保存文件，接着在终端中执行
```shell{.line-numbers}
source ~/.bashrc
```
或者退出当前终端再起一个终端。 这个办法的好处是把代理服务器永久保存了，下次就可以直接用了。
或者通过设置alias简写来简化操作，每次要用的时候输入setproxy，不用了就unsetproxy。
```vim{.line-numbers}
alias setproxy="export ALL_PROXY=socks5://127.0.0.1:1080"
alias unsetproxy="unset ALL_PROXY"
alias ip="curl -i http://ip.cn"
```