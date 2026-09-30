# python-sdk-sandbox

Sandbox for exercising a Python SDK cloned into `sdk/`.

## Goal

The goal of this project is to exercise the python sdk the same way our users will do. The only difference is that we have installed it as a "live" dependency
that lives in "/sdk". That way, when the tests find a bug, we can fix it from within this project.

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

## Directory structure

- ./sdk: Where the SDK lives. It's a live clone of the repository of the SDK. If a bug is found, it can be fixed there.
- ./tests: Where the tests for the SDK live.