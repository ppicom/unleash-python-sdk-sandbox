# python-sdk-sandbox

Sandbox for exercising a Python SDK cloned into `sdk/`.

## Setup

```sh
mise trust && mise install
# set SDK_REPO in mise.toml, then:
mise run sdk:clone   # clones into sdk/ and adds it as an editable dependency
mise run sync
```

## Usage

```sh
mise run run example.py   # run scripts/example.py
mise run test
mise run lint
mise run fmt
mise run sdk:pull         # update the SDK clone
```

The SDK is installed in editable mode, so changes in `sdk/` show up in scripts immediately.
