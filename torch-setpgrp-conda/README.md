# Torch setpgrp Conda bug demo

Python hangs if you do ALL of the following:

- Use Miniconda (passes with `python -m venv`)
- Create environment with Python 3.13 (passes with 3.12)
- Run python code via `subprocess.Popen` with `preexec_fn=os.setpgrp` (passes without `os.setpgrp`)
- Python code contains `import torch` (passes without it)

Combining all of these results in the subprocess hanging.

Changing any one of the conditions allows it to pass.

## Steps to Reproduce (Conda with Python 3.13)

The following is all on macOS Sequoia 15.5.

```shell
% brew install --cask miniconda
% conda init zsh
```

(Or: `conda init bash`.)

Open new shell.

Run all of the following From this directory.

```shell
% conda create -n "torch-setpgr-3.13" python=3.13 numpy pytorch -c conda-forge -y
% conda activate torch-setpgr-3.13
% python torch-setpgrp-test.py
Testing YES preexec_fn=os.setpgrp, NO import torch...
=== SUCCESS: YES os.setpgrp, NO torch import
PASS
Testing NO preexec_fn=os.setpgrp, YES import torch...
=== SUCCESS: NO os.setpgrp, YES import torch
PASS
Testing YES preexec_fn=os.setpgrp, YES import torch...
FAIL: Process timed out after 20 seconds
% conda deactivate
```

Only the last case fails, where we have both `os.setpgrp` and `import torch`.

(Fwiw `os.setpgid` results in the same behavior.)

## Working example: Conda with Python 3.12

```shell
% conda create -n "torch-setpgr-3.12" python=3.12 numpy pytorch -c conda-forge -y
% conda activate torch-setpgr-3.12
% python torch-setpgrp-test.py
Testing YES preexec_fn=os.setpgrp, NO import torch...
=== SUCCESS: YES os.setpgrp, NO torch import
PASS
Testing NO preexec_fn=os.setpgrp, YES import torch...
=== SUCCESS: NO os.setpgrp, YES import torch
PASS
Testing YES preexec_fn=os.setpgrp, YES import torch...
=== SUCCESS: YES os.setpgrp, YES import torch
PASS
% conda deactivate
```

All cases pass.

## Working example: Venv with Python 3.13

First, make sure you have python 3.13 installed locally, e.g. on Mac:

```shell
% brew install python@3.13
% python3.13 --version
Python 3.13.5
```

Then make a local `.venv`:

```shell
% python3.13 -m venv .venv
(.venv) % source .venv/bin/activate
(.venv) % pip install numpy torch
# For me, it installed numpy-2.3.2 and torch-2.7.1
(.venv) % python torch-setpgrp-test.py
% python torch-setpgrp-test.py
Testing YES preexec_fn=os.setpgrp, NO import torch...
=== SUCCESS: YES os.setpgrp, NO torch import
PASS
Testing NO preexec_fn=os.setpgrp, YES import torch...
=== SUCCESS: NO os.setpgrp, YES import torch
PASS
Testing YES preexec_fn=os.setpgrp, YES import torch...
=== SUCCESS: YES os.setpgrp, YES import torch
PASS
% deactivate
```

All cases pass.

(Fwiw also tested via `poyenv virtualenv`, and it works fine with that, too.)
