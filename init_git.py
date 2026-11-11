import subprocess
import sys


def run(cmd):
    print(f"👉 正在执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 错误: {result.stderr}")
        sys.exit(1)
    print(result.stdout)


def main():
    print("🚀 开始初始化 Nova-Orbit 企业级 Git 仓库...")

    # 1. 初始化仓库
    run(["git", "init"])
    run(["git", "branch", "-M", "main"])

    # 2. 配置换行符规范（Windows 必备）
    run(["git", "config", "core.autocrlf", "false"])

    # 3. 添加所有文件并首次提交
    run(["git", "add", "."])
    run(["git", "commit", "-m", "feat: initial release of Nova-Orbit AI chat UI framework"])

    print("\n✅ 本地 Git 初始化完成！")
    print("====================================")
    print("🔗 接下来请执行以下两步关联远程仓库并推送：")
    print("   1. git remote add origin https://github.com/eagleye-china/nova-orbit.git")
    print("   2. git push -u origin main")
    print("====================================")
    print("🏷️ 发布正式版时，只需打标签即可自动触发发布流水线：")
    print("   1. git tag v0.1.0")
    print("   2. git push origin v0.1.0")


if __name__ == "__main__":
    main()