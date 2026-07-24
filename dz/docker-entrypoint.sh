#!/usr/bin/env bash
set -euo pipefail

ARGS=()
BROWSERS_SPEC=""
browser_set=false
skip_next=false
skip_browsers=false

for arg in "$@"; do
  if $skip_next; then
    ARGS+=("--selenium-browser" "$arg")
    browser_set=true
    skip_next=false
    continue
  fi

  if $skip_browsers; then
    BROWSERS_SPEC="$arg"
    skip_browsers=false
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
    --browsers)
      skip_browsers=true
      ;;
    --browsers=*)
      BROWSERS_SPEC="${arg#*=}"
      ;;
    --headed)
      ARGS+=("--selenium-headed")
      ;;
    *)
      ARGS+=("$arg")
      ;;
  esac
done

run_pytest() {
  python -m pytest -c pytest.ini tests/selenium_tests "${ARGS[@]}" "$@"
}

if [[ -n "$BROWSERS_SPEC" ]]; then
  IFS=',' read -ra browser_entries <<< "$BROWSERS_SPEC"
  for entry in "${browser_entries[@]}"; do
    IFS=':' read -r browser_name browser_version <<< "$entry"
    echo "Running tests on ${browser_name} ${browser_version}..."
    run_pytest --selenium-browser "$browser_name" --browser_version "$browser_version"
  done
else
  if ! $browser_set; then
    ARGS=(--selenium-browser chrome "${ARGS[@]}")
  fi
  run_pytest
fi
