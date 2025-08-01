import subprocess  # noqa: S404
import sys

import dotenv
import git
import github

import pbi_parsers


def create_release() -> None:
    token = dotenv.get_key(dotenv_path=".env", key_to_get="GITHUB_TOKEN")
    if not token:
        msg = "GITHUB_TOKEN not found in .env file."
        raise ValueError(msg)
    token = github.Auth.Token(token=token)
    api = github.Github(auth=token)
    last_commit_message = git.Repo(".").head.commit.message
    remote_repo = api.get_user().get_repo("pbi_parsers")
    version = pbi_parsers.__version__
    release = remote_repo.create_git_release(
        tag=f"v{version}",
        name=f"Release {version}",
        message=f"Release {version}.\n\n{last_commit_message}",
        draft=False,
        prerelease=False,
    )
    release.upload_asset(
        path=f"dist/pbi_parsers-{version}-py3-none-any.whl",
        name=f"pbi_parsers-{version}-py3-none-any.whl",
        label=f"pbi_parsers-{version}-py3-none-any.whl",
    )
    release.upload_asset(
        path=f"dist/pbi_parsers-{version}.tar.gz",
        name=f"pbi_parsers-{version}.tar.gz",
        label=f"pbi_parsers-{version}.tar.gz",
    )


def tagger() -> None:
    """Tags the current commit with the version from pbi_parsers.

    This is useful for creating a release tag in the repository.

    Raises:
        ValueError: If the pbi_parsers version is not set.

    """
    if not pbi_parsers.__version__:
        msg = "pbi_parsers version is not set."
        raise ValueError(msg)

    current_version = f"v{pbi_parsers.__version__}"
    print(f"Tagging version {current_version} in the repository.")
    repo = git.Repo(".")
    existing_tags = [t.name for t in repo.tags]

    if current_version in existing_tags:
        print(f"Tag {current_version} already exists.")
        return

    repo.create_tag(current_version, message=f"Release {pbi_parsers.__version__}")
    print(f"Tag {current_version} created successfully.")


def builder() -> None:
    repo = git.Repo(".")
    existing_tags = [t.commit for t in repo.tags]
    if repo.head.commit not in existing_tags:
        return

    try:
        command = [sys.executable, "-m", "build", "."]
        result = subprocess.run(command, check=True, capture_output=True, text=True)  # noqa: S603
        print("Build successful!")
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error during build process: {e}")
        print("STDOUT:")
        print(e.stdout)
        print("STDERR:")
        print(e.stderr)
    except FileNotFoundError:
        print(f"Error: Python executable '{sys.executable}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise ValueError from e


def push_docs() -> None:
    command = ["mkdocs", "gh-deploy", "--clean", "-f", "docs/mkdocs.yml"]
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)  # noqa: S603
        print("Documentation pushed successfully!")
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error during documentation push: {e}")
        print("STDOUT:")
        print(e.stdout)
        print("STDERR:")
        print(e.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise ValueError from e


if __name__ == "__main__":
    tagger()
    builder()
    push_docs()
    create_release()
