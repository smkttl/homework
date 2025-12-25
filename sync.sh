#!/bin/bash
set -e
echo $ROOT
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$HOME/.sshtemp_homework"
cp "$ROOT/.ssh/id_rsa" "$HOME/.sshtemp_homework/id_rsa"
chmod 700 "$HOME/.sshtemp_homework/id_rsa"
export GIT_SSH_COMMAND="ssh -i $HOME/.sshtemp_homework/id_rsa -o StrictHostKeyChecking=no"
echo "SSH 私钥设置完毕"
#git config --global --add safe.directory $ROOT
git config user.name homework-bot
git config user.email 3121768621@qq.com
git add .
git commit -m "自动同步: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin master
rm -rf "$HOME/.sshtemp_homework"
echo "Press any key to continue..."
read
