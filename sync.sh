#!/bin/bash
set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo $ROOT
#git config --global --add safe.directory $ROOT
git config user.name homework-bot
git config user.email 3121768621@qq.com
git add .
git commit -m "自动同步: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin master
echo "Press any key to continue..."
read
