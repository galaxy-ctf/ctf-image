.PHONY: help

help:
	@egrep '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

sync-dry: ## Test push to AWS
	./cli53-linux-amd64 import --profile ctf --replace --wait --dry-run --file ctf.zone ZONEID
	@echo "If everything looks good, run: make sync-real"

sync-real: ## Real push to AWS
	./cli53-linux-amd64 import --profile ctf --replace --wait --file ctf.zone ZONEID

export: ## Sync to ctf.zone file
	./cli53-linux-amd64 export ZONEID --profile ctf > ctf.zone
