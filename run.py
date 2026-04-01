#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    result = subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        capture_output=True,
        text=True
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if check and result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    return result


def main():
    repo_root = Path(__file__).parent.resolve()

    print("=" * 60)
    print("GitHub 自动推送脚本")
    print("=" * 60)
    print(f"仓库路径: {repo_root}")
    print()

    print(">>> 检查 Git 状态...")
    status_result = run_command("git status --porcelain", cwd=repo_root, check=False)

    if not status_result.stdout.strip():
        print("没有检测到任何更改，无需推送。")
        return

    print("检测到以下更改：")
    print(status_result.stdout)

    commit_msg = input("\n请输入提交信息（直接回车使用默认信息）: ").strip()
    if not commit_msg:
        commit_msg = "Update: auto-sync changes"

    print(f"\n>>> 添加所有更改...")
    run_command("git add .", cwd=repo_root)

    print(f">>> 提交更改: {commit_msg}")
    run_command(f'git commit -m "{commit_msg}"', cwd=repo_root)

    print(">>> 推送到 GitHub...")
    run_command("git push -u origin main", cwd=repo_root)

    print()
    print("=" * 60)
    print("推送完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
