#!/usr/bin/env bash
set -euo pipefail

# Empaqueta el HTML de maqueta y el módulo de interacción junto con el Worker.
root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
node "$root/scripts/build.mjs"

