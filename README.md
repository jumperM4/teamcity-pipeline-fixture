# TeamCity pipeline fixture

This repository is a small deterministic Python project for learning and
testing TeamCity. Its first green build exercises the complete path from Git
checkout to test reporting and artifact publication.

## What the pipeline produces

- pytest results in `build/test-results/pytest.xml`;
- build metadata in `build/artifacts/summary.json`;
- a non-zero process exit code when an application test fails.

No credentials or environment-specific paths are stored in the repository.

## Run locally

The project requires Python 3.11 or newer. On Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -e ".[test]"
.venv/bin/python -m pytest --junitxml=build/test-results/pytest.xml
.venv/bin/python scripts/create_artifact.py
```

On Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --disable-pip-version-check -e ".[test]"
.\.venv\Scripts\python.exe -m pytest --junitxml=build/test-results/pytest.xml
.\.venv\Scripts\python.exe .\scripts\create_artifact.py
```

Expected result: 9 tests pass, a JUnit-compatible XML report and a JSON
artifact are created under `build/`.

## Configure the first TeamCity pipeline

Create `Python Fixture Pipeline` under the `Local Learning` project and connect
this public Git repository. Keep `main` as the default branch. Add one job named
`Tests and artifact` and run it on the Linux Agent.

Use a Script step with the following content:

```bash
set -eu
python3 -m venv .venv
.venv/bin/python -m pip install --disable-pip-version-check -e ".[test]"
.venv/bin/python -m pytest --junitxml=build/test-results/pytest.xml
.venv/bin/python scripts/create_artifact.py \
  --build-number "%build.number%" \
  --revision "%build.vcs.number%"
```

Configure XML report processing for:

```text
build/test-results/*.xml
```

Configure the artifact rule:

```text
build/artifacts/** => fixture-output
```

Run the pipeline manually once before enabling its VCS trigger. The acceptance
result is a successful build with 9 tests visible in TeamCity and a downloadable
`fixture-output/summary.json` artifact.

If `python3` is unavailable, fix the Agent image or select an Agent that declares
a compatible Python capability. Do not install tools silently during Agent
registration or hide the incompatibility with retries.

## Controlled follow-up scenarios

Keep the initial commit green. Add later scenarios as isolated commits so each
TeamCity result has one intentional cause:

1. Change an expected calculator result to create a deterministic test failure.
2. Revert the failure and confirm that TeamCity marks the test as fixed.
3. Add a feature branch and verify branch discovery and result isolation.
4. Enable a VCS trigger and verify that one commit starts one pipeline run.
5. Open a pull request and verify the selected revision and published status.
6. Change the artifact path to exercise missing-artifact diagnostics, then
   restore it in a separate commit.

Never commit TeamCity access tokens, Git provider credentials, local virtual
environments, reports, or generated artifacts.
