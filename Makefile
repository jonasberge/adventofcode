SRC_DIR=src
TEST_DIR=test
INPUTS_DIR=inputs
EXAMPLES_DIR="$(INPUTS_DIR)/examples"
TEMPLATE_DIR=template

PREFIX_DAY=day
PREFIX_TEST=test_day

TEMPLATE_DAY="$(TEMPLATE_DIR)/$(PREFIX_DAY)_x.py"
TEMPLATE_TEST="$(TEMPLATE_DIR)/$(PREFIX_TEST)_x.py"

OPEN=subl
TEST=venv/bin/pytest

include .env

# https://stackoverflow.com/a/14061796
ifeq (touch,$(firstword $(MAKECMDGOALS)))
	ARG_DAY := $(wordlist 2,2,$(MAKECMDGOALS))
	TARGET_DAY := "$(SRC_DIR)/$(PREFIX_DAY)_$(ARG_DAY).py"
	TARGET_TEST := "$(TEST_DIR)/$(PREFIX_TEST)_$(ARG_DAY).py"
  $(eval $(ARG_DAY):;@:)  # indent with spaces so this is not a target.
else ifeq (test,$(firstword $(MAKECMDGOALS)))
	ARG_DAY := $(wordlist 2,2,$(MAKECMDGOALS))
  $(eval $(ARG_DAY):;@:)
endif

venv:
	python3 -m venv venv

install:
	pip install -U pip
	pip install -r requirements.txt

touch:
	test ! -f $(TARGET_DAY)
	test ! -f $(TARGET_TEST)
	cp "$(TEMPLATE_DAY)" $(TARGET_DAY)
	cp "$(TEMPLATE_TEST)" $(TARGET_TEST)
	sed -i "s/'''?x'''/$(ARG_DAY)/g" $(TARGET_DAY)
	command -v $(OPEN) && $(OPEN) $(TARGET_TEST) $(TARGET_DAY) || true
	$(eval EXAMPLES_DIR_DAY="$(EXAMPLES_DIR)/$(PREFIX_DAY)-$(ARG_DAY)")
	mkdir -p $(INPUTS_DIR) $(EXAMPLES_DIR_DAY)
	touch "$(EXAMPLES_DIR_DAY)/example-1.txt"
	curl -f -b "session=$(SESSION)" \
		"https://adventofcode.com/2020/day/$(ARG_DAY)/input" \
		-o "$(INPUTS_DIR)/$(PREFIX_DAY)-$(ARG_DAY).txt"

test:
	@if [ -z "${ARG_DAY}" ]; then \
		$(TEST); \
	else \
		$(TEST) "$(TEST_DIR)/$(PREFIX_TEST)_$(ARG_DAY).py"; \
	fi

.PHONY: venv install new test
