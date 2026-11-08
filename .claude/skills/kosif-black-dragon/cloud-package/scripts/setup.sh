#!/usr/bin/env bash
# Same as: python3 scripts/dragon.py setup [--full|--gpu]
exec python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/dragon.py" setup "$@"
