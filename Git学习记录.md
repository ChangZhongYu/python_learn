Git 版本控制工具
三种工作区：
| 区域     | 文件状态         | 命令       | 说明         |
| -------- | ---------------- | ---------- | ------------ |
| 工作区   | 已修改（未跟踪） | git add    | 加入暂存区   |
| 缓存区   | 已暂存           | git commit | 提交本地仓库 |
| 本地仓库 | 已提交           |            |              |
其他命令：

``` python
# 获取文件状态
git status

# 提交并说明
git commit -m '说明' |-am 缓存并提交  

# 查看提交日志
git log |--pretty=oneline 格式化展示

git reflog 查看历史操作

# 对比工作区文件和仓库文件
gti diff HEAD -- 对比文件名称

# 撤销暂存
git restore --staged 文件名

# 撤销上一次命令
git reset HEAD 文件名（）

# 版本回退
git reset --hard HEAD^ | ^数量表示回退几个版本 | ~10 回退10个版本 

git reset --hard commitID 回退到指定ID的版本

# 切换分支
git checkout 分支名

# 删除分支
git branch -d|-D 分支名 -D强制删除

# 合并分支
gti merge 被合并的分支

```

.gitignore 不管理的文件

``` python
# 配置SSH公钥 rsa 非对称秘钥算法 目录 cat ~/.ssh/id_rsa.pub
ssh-keygen -t rsa

# 查看配置是否成功
ssh -T git@仓库地址

# 配置远程仓库
git remote add 远程仓库名（origin） 地址

# 查看
git remote

# 推送
git push [-f][--set-upstream]仓库名 分支 [强制推送][对应关系，仓库名后加分支]

# 查看分支对应关系
git branch -vv

# 从远处仓库拷贝
git clone

# 抓取（更新不合并）
git fetch 

# 拉取（合并本地代码）
git pull
```

在Idea中使用git
 1. 配置idea
 2. 初始化本地仓库
 3. 配置忽视文件
 4. 提交或推送

