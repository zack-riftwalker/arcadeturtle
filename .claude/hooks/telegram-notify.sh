#!/usr/bin/env bash
# Stop hook: send a Telegram message when Claude finishes.
# Needs TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in the environment (never committed).
# If either is missing, or the request fails, it exits 0 silently so it never disrupts the session.

[ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ] || exit 0

input=$(cat)
repo=$(basename "${CLAUDE_PROJECT_DIR:-$PWD}")
branch=$(git -C "${CLAUDE_PROJECT_DIR:-$PWD}" rev-parse --abbrev-ref HEAD 2>/dev/null)
last=$(printf '%s' "$input" | jq -r '.last_assistant_message // empty' 2>/dev/null | head -c 600)

text="Claude Code finished
repo: ${repo}${branch:+ (${branch})}"
[ -n "$last" ] && text="${text}

${last}"

curl -sS --max-time 10 -o /dev/null \
  "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
  --data-urlencode "text=${text}" 2>/dev/null

exit 0
