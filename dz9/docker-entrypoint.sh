#!/usr/bin/env bash
set -euo pipefail

ARGS=()
browser_set=false
skip_next=false

for arg in "$@"; do
  if $skip_next; then
    ARGS+=("--selenium-browser" "$arg")
    browser_set=true
    skip_next=false
    continue
  fi

  case "$arg" in
    --browser)
      skip_next=true
      ;;
    --browser=*)
      ARGS+=("--selenium-browser=${arg#*=}")
      browser_set=true
      ;;
    --selenium-browser|--selenium-browser=*)
      ARGS+=("$arg")
      browser_set=true
      ;;
    --headed)
      ARGS+=("--selenium-headed")
      ;;
    *)
      ARGS+=("$arg")
      ;;
  esac
done

if ! $browser_set; then
  ARGS=(--selenium-browser chrome "${ARGS[@]}")
fi

exec python -m pytest -c pytest.ini tests/selenium_tests "${ARGS[@]}"
