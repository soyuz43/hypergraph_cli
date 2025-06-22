SHELL := /bin/bash

ENV_DIR := hgcli-env
ACTIVATE_POSIX := source ./$(ENV_DIR)/Scripts/activate
ACTIVATE_PWSH := .\\$(ENV_DIR)\\Scripts\\Activate.ps1
ACTIVATE_CMD := $(ENV_DIR)\Scripts\activate.bat

env:
	@echo " Virtual Environment Activation Assistant"
	@if [ -f "./$(ENV_DIR)/Scripts/activate" ]; then \
		echo "Detected POSIX-compatible shell (bash/zsh)..."; \
		echo ""; \
		echo "To activate your environment, run this:"; \
		echo ""; \
		echo "  $(ACTIVATE_POSIX)"; \
	else \
		echo "You're likely in PowerShell or CMD."; \
		echo ""; \
		echo "Use one of the following depending on your shell:"; \
		echo ""; \
		echo "  PowerShell:"; \
		echo "    $(ACTIVATE_PWSH)"; \
		echo ""; \
		echo "  CMD.exe:"; \
		echo "    $(ACTIVATE_CMD)"; \
	fi
	@echo ""
	@echo "Note: Make cannot persist shell changes, so you must run the command manually."
