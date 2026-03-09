# IASNE/Backend 重构文档站

本目录是独立可部署文档仓库结构，目标仓库为：

`git@github.com:ListenToATree/docs.git`

## 本地预览

```bash
cd docs
python -m pip install --upgrade pip
pip install mkdocs mkdocs-material pymdown-extensions
mkdocs serve
```

浏览器访问 `http://127.0.0.1:8000`。

## 构建静态站点

```bash
cd docs
mkdocs build
```

构建结果在 `docs/site/`。

## 首次推送到目标仓库

```bash
cd docs
git init
git branch -M main
git remote add origin git@github.com:ListenToATree/docs.git
git add .
git commit -m "docs: initial product and tech refactor documentation"
git push -u origin main
```

## GitHub Pages 部署

该目录已包含 `.github/workflows/deploy.yml`，推送到 `main` 后会自动构建并发布 GitHub Pages。

需要在 GitHub 仓库设置中启用 Pages（Source: GitHub Actions）。
