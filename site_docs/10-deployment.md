# 部署说明（GitHub）

目标仓库：`git@github.com:ListenToATree/docs.git`

## 一、文档站技术方案

本目录使用 MkDocs + Material 主题，支持：
- 本地预览
- 静态构建
- GitHub Actions 自动部署到 Pages

## 二、首次部署步骤

```bash
cd docs
python -m pip install --upgrade pip
pip install mkdocs mkdocs-material pymdown-extensions
mkdocs build

# 推送到目标仓库
git init
git branch -M main
git remote add origin git@github.com:ListenToATree/docs.git
git add .
git commit -m "docs: initial product and tech refactor documentation"
git push -u origin main
```

## 三、自动部署

仓库内已提供：`.github/workflows/deploy.yml`

推送 `main` 后会自动：
1. 安装依赖
2. 执行 `mkdocs build`
3. 发布到 GitHub Pages

## 四、可选一键脚本

```bash
cd docs
bash scripts/push_to_target_repo.sh
```

## 五、注意事项

1. 需要当前机器具备目标仓库 SSH 推送权限。
2. 需在 GitHub 仓库设置中启用 Pages（GitHub Actions 作为来源）。
3. 文档更新建议走 PR 流程并绑定里程碑。 
