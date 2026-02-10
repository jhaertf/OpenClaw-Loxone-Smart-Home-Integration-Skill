#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_PATH="${LOXONE_CONFIG_PATH:-$BASE_DIR/config.json}"
ACTIONS_PATH="${LOXONE_ACTIONS_PATH:-$BASE_DIR/actions.json}"

usage() {
  cat <<USAGE
Usage:
  $0 list_actions
  $0 run_action <action_id>
USAGE
}

require_file() {
  local f="$1"
  [[ -f "$f" ]] || { echo "Missing file: $f"; exit 1; }
}

read_secret_file() {
  local f="$1"
  [[ -f "$f" ]] || { echo "Missing secret file: $f"; exit 1; }
  <"$f"
}

call_loxone() {
  local host="$1" user="$2" pass="$3" control="$4" cmd="$5"
  curl -sk -u "$user:$pass" "${host}/jdev/sps/io/${control}/${cmd}"
}

cmd="${1:-}"
case "$cmd" in
  list_actions)
    require_file "$ACTIONS_PATH"
    jq -r '.actions | keys[]' "$ACTIONS_PATH"
    ;;
  run_action)
    action_id="${2:-}"
    [[ -n "$action_id" ]] || { usage; exit 1; }
    require_file "$CONFIG_PATH"
    require_file "$ACTIONS_PATH"

    host_file=$(jq -r '.hostFile // empty' "$CONFIG_PATH")
    user=$(jq -r '.user // empty' "$CONFIG_PATH")
    pass_file=$(jq -r '.passwordFile // empty' "$CONFIG_PATH")

    control=$(jq -r --arg id "$action_id" '.actions[$id].control // empty' "$ACTIONS_PATH")
    command=$(jq -r --arg id "$action_id" '.actions[$id].command // empty' "$ACTIONS_PATH")
    post_script=$(jq -r --arg id "$action_id" '.actions[$id].post_action_script // empty' "$ACTIONS_PATH")

    [[ -n "$host_file" && -n "$user" && -n "$pass_file" && -n "$control" && -n "$command" ]] || {
      echo "Invalid mapping/config for action: $action_id"; exit 1;
    }

    host=$(read_secret_file "$host_file")
    pass=$(read_secret_file "$pass_file")

    call_loxone "$host" "$user" "$pass" "$control" "$command" >/dev/null
    echo "OK: action '$action_id' executed"

    if [[ -n "$post_script" ]]; then
      if [[ -x "$post_script" ]]; then
        "$post_script" || true
      else
        echo "WARN: post_action_script not executable: $post_script"
      fi
    fi
    ;;
  *)
    usage
    exit 1
    ;;
esac
