# Collaboration

## Concepts

- Channels: persistent team rooms with shared projects, notes, and voice collaboration.
- Contacts/private calls: ad-hoc sessions outside channels.
- Project sharing: guests interact with a host's project/session according to Zed collaboration behavior.

Before guiding, identify whether the user wants to share a project, join a channel, start voice, pair edit, or solve permissions/network/audio issues.

## Safety and access

- Confirm organization policy/admin controls before enabling collaboration for company code.
- Share only the intended project root. Avoid opening a parent directory containing unrelated repositories, credentials, or personal files.
- Explain participant access and host dependency using current docs; do not assume collaboration grants source-control or production access.
- Treat terminal/task/agent use in a collaborative session as potentially impactful. Confirm who can trigger operations and review before executing secrets-bearing commands.
- Use least privilege and end/remove access when the session finishes.

## Troubleshooting

1. Verify sign-in/account and organization policy.
2. Check Zed version compatibility and network/firewall restrictions.
3. For project sharing, confirm host remains online and correct root is shared.
4. For voice, check OS microphone permission, selected input/output, and competing applications.
5. Collect logs only after reproducing; redact channel names, participant data, source paths, and tokens.

Official sources: [Collaboration Overview](https://zed.dev/docs/collaboration/overview), [Channels](https://zed.dev/docs/collaboration/channels), [Contacts and Private Calls](https://zed.dev/docs/collaboration/contacts-and-private-calls), [Admin Controls](https://zed.dev/docs/business/admin-controls).
