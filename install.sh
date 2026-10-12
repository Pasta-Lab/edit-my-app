#!/usr/bin/env bash
# Installs instruction files only. Compatible with macOS's bundled Bash.
set -euo pipefail

omniform_fail() { printf 'Edit My App: %s\n' "$*" >&2; exit 1; }

omniform_no_symlink_parents() {
    local omniform_part="$1"
    while [[ "$omniform_part" != / ]]; do
        [[ ! -L "$omniform_part" ]] || omniform_fail "Symlinked path: $omniform_part. Choose its real location."
        omniform_part=$(dirname "$omniform_part")
    done
}

omniform_cleanup() {
    # Only this invocation's mktemp directory may be removed; never the skill.
    if [[ -n "${omniform_stage:-}" ]]; then
        case "$omniform_stage" in
            "$omniform_parent"/.edit-my-app-stage.????????)
                [[ -L "$omniform_stage" ]] || rm -rf -- "$omniform_stage"
                ;;
        esac
    fi
    if [[ "${omniform_lock_owned:-0}" == 1 ]]; then
        rmdir "$omniform_parent/.edit-my-app-install.lock" 2>/dev/null || true
    fi
}

omniform_main() {
    local omniform_agent=codex omniform_source='' omniform_destination=''
    local omniform_arg omniform_script omniform_file omniform_from omniform_to
    local omniform_base='https://raw.githubusercontent.com/Pasta-Lab/edit-my-app/main'
    while [[ $# -gt 0 ]]; do
        omniform_arg=$1
        case "$omniform_arg" in
            --agent|--dest|--source)
                [[ $# -ge 2 && -n "$2" ]] || omniform_fail "Missing value after $omniform_arg."
                case "$omniform_arg" in
                    --agent) omniform_agent=$2 ;;
                    --dest) omniform_destination=$2 ;;
                    --source) omniform_source=$2 ;;
                esac
                shift 2 ;;
            --help|-h)
                printf '%s\n' 'Usage: bash install.sh [--agent codex|claude] [--dest /skills/parent] [--source /checkout]'
                printf '%s\n' 'Installs text instructions only. Existing installations are never overwritten.'
                return ;;
            *) omniform_fail "Unknown option: $omniform_arg" ;;
        esac
    done
    case "$omniform_agent" in
        codex) omniform_parent=${omniform_destination:-"${HOME:?HOME is required}/.agents/skills"} ;;
        claude) omniform_parent=${omniform_destination:-"${HOME:?HOME is required}/.claude/skills"} ;;
        *) omniform_fail 'Choose --agent codex or claude, or use --dest for another host.' ;;
    esac
    while [[ "$omniform_parent" != / && "$omniform_parent" == */ ]]; do omniform_parent=${omniform_parent%/}; done
    case "$omniform_parent" in
        ''|/|*/../*|*/..|*/./*|*/.|*$'\n'*) omniform_fail 'Use an absolute skills parent directory without dot segments.' ;;
        /*) ;;
        *) omniform_fail 'The skills parent directory must be absolute.' ;;
    esac
    omniform_no_symlink_parents "$omniform_parent"
    omniform_target="$omniform_parent/edit-my-app"
    [[ ! -L "$omniform_target" ]] || omniform_fail "Existing skill is a symlink; left untouched: $omniform_target"
    if [[ -e "$omniform_target" ]]; then
        printf 'Already exists; left untouched: %s\nMove this skill aside before updating it.\n' "$omniform_target"
        return
    fi

    # Local checkout installs stay offline. Piped installs fetch only known text files.
    if [[ -z "$omniform_source" && -n "${BASH_SOURCE[0]:-}" && -f "${BASH_SOURCE[0]}" ]]; then
        omniform_script=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
        omniform_source=$omniform_script
    fi
    if [[ -n "$omniform_source" ]]; then
        [[ -d "$omniform_source/skills/edit-my-app" ]] || omniform_fail 'Source checkout has no Edit My App skill.'
        omniform_source=$(cd "$omniform_source" && pwd -P)
    else
        command -v curl >/dev/null || omniform_fail 'HTTPS download needs curl; alternatively use a downloaded checkout.'
    fi

    mkdir -p "$omniform_parent"
    mkdir "$omniform_parent/.edit-my-app-install.lock" 2>/dev/null ||
        omniform_fail "Another install may be running. Check $omniform_parent/.edit-my-app-install.lock before retrying."
    omniform_lock_owned=1
    trap omniform_cleanup EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM
    omniform_stage=$(mktemp -d "$omniform_parent/.edit-my-app-stage.XXXXXXXX")
    mkdir -p "$omniform_stage/edit-my-app/references"
    local omniform_files=(SKILL.md references/workflow.md references/tools.md
        references/macos.md references/ios.md references/windows.md references/linux.md references/android.md LICENSE)
    for omniform_file in "${omniform_files[@]}"; do
        omniform_to="$omniform_stage/edit-my-app/$omniform_file"
        omniform_from="skills/edit-my-app/$omniform_file"
        if [[ -n "$omniform_source" ]]; then
            omniform_no_symlink_parents "$omniform_source/$omniform_from"
            [[ -f "$omniform_source/$omniform_from" ]] || omniform_fail "Missing file: $omniform_from"
            cp "$omniform_source/$omniform_from" "$omniform_to"
        else
            curl --fail --silent --show-error --location --proto '=https' --proto-redir '=https' \
                --connect-timeout 15 --max-time 60 "$omniform_base/$omniform_from" --output "$omniform_to"
        fi
        [[ -s "$omniform_to" ]] || omniform_fail "Empty file: $omniform_file"
    done
    [[ "$(head -n 1 "$omniform_stage/edit-my-app/SKILL.md")" == --- ]] || omniform_fail 'Invalid skill header.'
    grep -qx 'name: edit-my-app' "$omniform_stage/edit-my-app/SKILL.md" || omniform_fail 'Unexpected skill name.'
    [[ ! -e "$omniform_target" && ! -L "$omniform_target" ]] || omniform_fail 'Destination appeared during installation; left untouched.'
    mv "$omniform_stage/edit-my-app" "$omniform_target"
    printf 'Installed Edit My App: %s\n' "$omniform_target"
    printf '%s\n' 'No apps, analysis tools, SDKs, or agent settings were changed.'
    printf '%s\n' 'Start a new agent chat and say: Use edit-my-app to change my app.'
}

# Keeping all writes inside this function also avoids partially executing a
# truncated download that never reaches this final invocation.
omniform_main "$@"
