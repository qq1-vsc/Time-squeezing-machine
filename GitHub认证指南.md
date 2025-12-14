# 🔐 GitHub 认证指南 - 完成上传

## 当前状态
✅ 本地 git 已初始化
✅ 所有文件已提交
⚠️ **需要：GitHub 认证完成推送**

---

## 方案选择（推荐二选一）

### 🟢 方案 A：使用 GitHub 个人访问令牌（推荐）

#### 第 1 步：创建 Personal Access Token
1. 打开 https://github.com/settings/tokens
2. 点击 **"Generate new token"** → **"Generate new token (classic)"**
3. 填写信息：
   - **Token name**: `wallfacer-push`
   - **Expiration**: 选择合适期限（如 30 days 或 90 days）
   - **Select scopes**: 勾选 **repo** （完整仓库访问）
4. 点击 **"Generate token"** 
5. 复制生成的令牌（**只显示一次，一定要复制！**）

#### 第 2 步：在本地配置令牌
运行以下命令：

```powershell
cd "e:\Wallfacer System"
git push -u origin main
```

系统会提示输入用户名和密码：
- **Username**: `qq1-vsc`
- **Password**: 粘贴刚才复制的 Token（不是密码！）

---

### 🔵 方案 B：配置 Git Credential Manager

#### 第 1 步：设置凭证存储
```powershell
git config --global credential.helper wincred
```

#### 第 2 步：首次推送时输入凭证
```powershell
cd "e:\Wallfacer System"
git push -u origin main
```

系统会弹出 GitHub 登录框：
- 输入 GitHub 用户名：`qq1-vsc`
- 输入 Personal Access Token（如使用方案 A）或 GitHub 密码

---

### ⚫ 方案 C：使用 SSH 密钥（高级）

如果你已配置 SSH 密钥，改用：

```powershell
cd "e:\Wallfacer System"
git remote set-url origin git@github.com:qq1-vsc/Time-squeezing-machine.git
git push -u origin main
```

---

## 逐步操作（推荐方案 A）

### 第 1 步：创建 Token
访问：https://github.com/settings/tokens

![Step 1: Click Settings](https://github.githubassets.com/images/help/settings/token_new.png)

1. 左侧栏点击 **"Developer settings"**
2. 选择 **"Personal access tokens"** → **"Tokens (classic)"**
3. 点击 **"Generate new token"** → **"Generate new token (classic)"**

### 第 2 步：配置 Token 权限
| 选项 | 配置 |
|------|------|
| Token name | wallfacer-push |
| Expiration | 90 days |
| **repo** | ✅ 全选 |
| **workflow** | ✅ (可选) |

### 第 3 步：复制 Token
- 会看到 `ghp_xxxxxxxxxxxxxxxxxxxxxx` 格式的字符串
- **立即复制！** 刷新后不可见
- 安全保存（不要分享）

### 第 4 步：在 PowerShell 中推送

```powershell
# 进入项目目录
cd "e:\Wallfacer System"

# 执行推送
git push -u origin main

# 提示输入时：
# 用户名: qq1-vsc
# 密码: 粘贴 Token（Ctrl+V）
```

---

## 常见问题

### Q1: "fatal: Permission denied"
**解决**：
- 检查 Token 是否过期
- 重新创建新 Token
- 验证用户名是否正确（`qq1-vsc`）

### Q2: "repository not found"
**解决**：
- 确认仓库名称正确：`qq1-vsc/Time-squeezing-machine`
- 验证仓库是否公开或你有访问权限

### Q3: 输入后仍然报权限错误
**解决**：
- 清除已保存的凭证：
  ```powershell
  git credential reject
  # 输入：
  # host=github.com
  # protocol=https
  # 按 Ctrl+D
  ```
- 重新执行 `git push -u origin main`

### Q4: Token 过期了
**解决**：
- 访问 https://github.com/settings/tokens
- 生成新 Token
- 重新执行 `git push -u origin main`

---

## 验证成功

推送成功后会看到：
```
Enumerating objects: 14, done.
Counting objects: 100% (14/14), done.
Delta compression using up to 8 threads
Compressing objects: 100% (10/10), done.
Writing objects: 100% (14/14), 3.16 KiB | 528.00 KiB/s, done.
Total 14 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/qq1-vsc/Time-squeezing-machine.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ **完成！** 访问 https://github.com/qq1-vsc/Time-squeezing-machine 查看

---

## 下次推送（更简单）

保存凭证后，后续只需：

```powershell
cd "e:\Wallfacer System"
git add .
git commit -m "更新: xxx"
git push
```

无需再输入密码！

---

## 🚀 推送完成后

1. 访问 GitHub 仓库检查代码
2. 更新仓库描述和 README
3. 添加 GitHub Pages（可选）
4. 分享链接给他人

---

**需要进一步帮助？** 让我知道！
