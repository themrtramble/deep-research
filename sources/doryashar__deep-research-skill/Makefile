.PHONY: help test test-classifier test-pressure smoke smoke-quick smoke-standard smoke-deep install-claude install-opencode clean lint

SKILL_SRC := $(CURDIR)/skill
CLAUDE_SKILL_DIR ?= $(HOME)/.claude/skills/deep-research
OPENCODE_SKILL_DIR ?= $(HOME)/.config/opencode/skills/deep-research

help:
	@echo "Targets:"
	@echo "  test              Run classifier + smoke tests (node --test)"
	@echo "  test-classifier   Classifier unit tests only"
	@echo "  test-pressure     Subagent pressure scenarios (TDD-for-skills)"
	@echo "  smoke             Run all smoke tests with cached fixtures"
	@echo "  smoke-quick       Quick-mode smoke test"
	@echo "  smoke-standard    Standard-mode smoke test"
	@echo "  smoke-deep        Deep-mode smoke test"
	@echo "  install-claude    Symlink skill/ -> $(CLAUDE_SKILL_DIR)"
	@echo "  install-opencode  Symlink skill/ -> $(OPENCODE_SKILL_DIR)"
	@echo "  clean             Remove research/ and .cache/"

test: test-classifier test-pressure

test-classifier:
	node --test tests/classifier/*.js

test-pressure:
	node tests/pressure/run_pressure.js

smoke: smoke-quick smoke-standard smoke-deep

smoke-quick:
	bash tests/smoke/run_quick.sh

smoke-standard:
	bash tests/smoke/run_standard.sh

smoke-deep:
	bash tests/smoke/run_deep.sh

install-claude:
	@mkdir -p $(dir $(CLAUDE_SKILL_DIR))
	@rm -f $(CLAUDE_SKILL_DIR)
	@ln -s $(SKILL_SRC) $(CLAUDE_SKILL_DIR)
	@echo "Linked $(SKILL_SRC) -> $(CLAUDE_SKILL_DIR)"

install-opencode:
	@mkdir -p $(dir $(OPENCODE_SKILL_DIR))
	@rm -f $(OPENCODE_SKILL_DIR)
	@ln -s $(SKILL_SRC) $(OPENCODE_SKILL_DIR)
	@echo "Linked $(SKILL_SRC) -> $(OPENCODE_SKILL_DIR)"

clean:
	rm -rf research/ .cache/

lint:
	node --check skill/scripts/classify.js skill/scripts/dedup_sources.js skill/scripts/validate_outputs.js tests/classifier/*.js tests/pressure/run_pressure.js
