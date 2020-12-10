SRC_DIR=src
TEST_DIR=test
TEMPLATE_DIR="template"

PREFIX_DAY=day
PREFIX_TEST=test_day

TEMPLATE_DAY="$(TEMPLATE_DIR)/$(PREFIX_DAY)_x.py"
TEMPLATE_TEST="$(TEMPLATE_DIR)/$(PREFIX_TEST)_x.py"

# https://stackoverflow.com/a/14061796
ifeq (new,$(firstword $(MAKECMDGOALS)))
	ARG_DAY := $(wordlist 2,2,$(MAKECMDGOALS))
	TARGET_DAY := "$(SRC_DIR)/$(PREFIX_DAY)_$(ARG_DAY).py"
	TARGET_TEST := "$(TEST_DIR)/$(PREFIX_TEST)_$(ARG_DAY).py"
  $(eval "$(ARG_DAY)":;@:)  # indent with spaces so this is not a target.
endif

new:
	test ! -f $(TARGET_DAY)
	test ! -f $(TARGET_TEST)
	cp "$(TEMPLATE_DAY)" $(TARGET_DAY)
	cp "$(TEMPLATE_TEST)" $(TARGET_TEST)
	sed -i "s/'''?x'''/$(ARG_DAY)/g" $(TARGET_DAY)
	command -v subl && subl $(TARGET_TEST) $(TARGET_DAY) || true

.PHONY: new
