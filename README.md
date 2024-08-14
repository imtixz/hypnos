Hypnos v0.0.1

Hypnos is a very simple self-hosted continuous deployment tool that uses docker for deployment. It listens for github webhooks and redeploys docker compose files when a new change is pushed.

Philosophy:
On my homelab, I want changes to be pushed to deployment everytime code is pushed to a branch. But -

1. I don't want to edit the content of a repository just to host it on my homelab (no github actions, no separate dockerfile or docker compose file etc.)
2. I don't want to manually take any action every time a change is pushed to that repository

Todo:

1. Write documentaiton on how to use hypnos
2. Accept the github webhook secret from an env var instead of hard coding
3. Add profile name in the repo (e.g. imtixz/hypnos instead of hypnos)
4. Add support for more branches other than main
5. Add the update command on the cli tool
