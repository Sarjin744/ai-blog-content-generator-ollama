"""
GitHub Remote Push Utility for Experiment 2
Course: 24CS2506 – Building Applications using GPT-4
Experiment 2: AI-Powered Blog Content Generator using Ollama
"""

import sys
import dulwich.porcelain as porcelain


def push_repo(remote_url: str, branch: str = "main"):
    """Pushes local repository commits to the specified GitHub remote repository."""
    print(f"[*] Target Remote: {remote_url}")
    print(f"[*] Target Branch: {branch}")

    try:
        repo = porcelain.open_repo_closing(".")
        with repo:
            # Check or set branch to main
            ref_name = f"refs/heads/{branch}".encode()
            head_commit = repo.head()
            repo.refs[ref_name] = head_commit

            print("[*] Pushing commit to remote repository...")
            porcelain.push(repo, remote_url, ref_name)
            print("[✓] Repository successfully pushed to GitHub!")
            return True
    except Exception as e:
        print(f"[!] Push failed: {e}")
        print("\nTip: For private repositories or HTTPS auth, provide your URL with a GitHub Personal Access Token (PAT):")
        print("  https://<YOUR_GITHUB_TOKEN>@github.com/<USERNAME>/<REPO_NAME>.git")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        remote = sys.argv[1]
    else:
        remote = input("Enter your GitHub repository URL (e.g. https://github.com/username/repo.git): ").strip()

    if not remote:
        print("Error: Remote URL cannot be empty.")
        sys.exit(1)

    success = push_repo(remote)
    sys.exit(0 if success else 1)
