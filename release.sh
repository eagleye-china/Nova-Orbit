#!/usr/bin/env bash
set -euo pipefail

echo "========================================="
echo "  🚀 语义化一键发版"
echo "========================================="
echo ""
echo "请选择版本类型："
echo "  1) patch  (bug修复 → v0.0.x)"
echo "  2) minor  (新功能 → v0.x.0)"
echo "  3) major  (破坏性变更 → vx.0.0)"
echo "  4) 预览（dry run，不发版）"
echo "  5) 退出"
echo ""
read -rp "输入数字 [1-5]: " choice

case "$choice" in
  1) BUMP="patch" ;;
  2) BUMP="minor" ;;
  3) BUMP="major" ;;
  4)
    echo "📋 预览模式..."
    uv tool run semantic-release --dry --no-push version
    exit 0
    ;;
  5) exit 0 ;;
  *) echo "❌ 无效选择"; exit 1 ;;
esac

echo ""
echo "📝 接下来写 commit 消息（规范格式）："
echo "  feat: 新功能"
echo "  fix: 修复bug"
echo "  feat!: 破坏性变更"
echo ""
read -rp "输入 commit 类型 (feat/fix/refactor/docs/chore): " ctype
read -rp "输入简短描述: " desc

if [[ "$BUMP" == "major" ]]; then
  MSG="${ctype}!: ${desc}"
else
  MSG="${ctype}: ${desc}"
fi

echo ""
echo "📋 确认操作："
echo "  bump: $BUMP"
echo "  commit: $MSG"
echo ""
read -rp "确认发布? (y/N): " ok
[[ "$ok" == "y" ]] || exit 0

git add -A
git commit -m "$MSG"
git push origin main

echo ""
echo "✅ 已推送！GitHub Actions 将自动："
echo "  1. 分析 commits → bump 版本"
echo "  2. 生成 CHANGELOG.md"
echo "  3. 打 tag → 触发 PyPI 发布"
echo ""
echo "📺 查看进度：https://github.com/$(git config remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/actions"