SHELL := /bin/sh

ENV_FILE ?= .env

ifeq ($(OS),Windows_NT)
DEFAULT_ENV_TARGET := env-pwsh
else
DEFAULT_ENV_TARGET := env-posix
endif

TARGET_SHELL ?= $(DEFAULT_ENV_TARGET)

.PHONY: env env-posix env-pwsh env-cmd env-check

env:
	@$(MAKE) $(TARGET_SHELL)

env-check:
	@test -f $(ENV_FILE) || (echo "[env] missing $(ENV_FILE)" >&2; exit 1)

env-posix: env-check
	@awk -F= 'function ltrim(s){sub(/^[ \t]+/,"",s);return s} \
	function rtrim(s){sub(/[ \t]+$$/,"",s);return s} \
	function trim(s){return rtrim(ltrim(s))} \
	function clean_key(k){sub(/^export[ \t]+/,"",k);return trim(k)} \
	function strip_quotes(v){if((v ~ /^".*"$$/) || (v ~ /^'\''.*'\''$$/)) return substr(v,2,length(v)-2);return v} \
	function escape(v){gsub(/\\/,"\\\\",v);gsub(/"/,"\\\"",v);return v} \
	/^[ \t]*#/ || /^[ \t]*$$/ {next} \
	{ key=clean_key($$1); val=trim(substr($$0, index($$0,"=")+1)); if(!key) next; \
	  val=escape(strip_quotes(val)); \
	  printf("export %s=\"%s\"\n", key, val); }' $(ENV_FILE)

env-pwsh: env-check
	@awk -F= 'function ltrim(s){sub(/^[ \t]+/,"",s);return s} \
	function rtrim(s){sub(/[ \t]+$$/,"",s);return s} \
	function trim(s){return rtrim(ltrim(s))} \
	function clean_key(k){sub(/^export[ \t]+/,"",k);return trim(k)} \
	function strip_quotes(v){if((v ~ /^".*"$$/) || (v ~ /^'\''.*'\''$$/)) return substr(v,2,length(v)-2);return v} \
	function escape(v){gsub(/`/,"``",v);gsub(/"/,"`\"",v);return v} \
	/^[ \t]*#/ || /^[ \t]*$$/ {next} \
	{ key=clean_key($$1); val=trim(substr($$0, index($$0,"=")+1)); if(!key) next; \
	  val=escape(strip_quotes(val)); \
	  printf("$$Env:%s = \"%s\"\n", key, val); }' $(ENV_FILE)

env-cmd: env-check
	@awk -F= 'function ltrim(s){sub(/^[ \t]+/,"",s);return s} \
	function rtrim(s){sub(/[ \t]+$$/,"",s);return s} \
	function trim(s){return rtrim(ltrim(s))} \
	function clean_key(k){sub(/^export[ \t]+/,"",k);return trim(k)} \
	function strip_quotes(v){if((v ~ /^".*"$$/) || (v ~ /^'\''.*'\''$$/)) return substr(v,2,length(v)-2);return v} \
	function escape(v){gsub(/%/,"%%",v);return v} \
	/^[ \t]*#/ || /^[ \t]*$$/ {next} \
	{ key=clean_key($$1); val=trim(substr($$0, index($$0,"=")+1)); if(!key) next; \
	  val=escape(strip_quotes(val)); \
	  printf("set %s=%s\n", key, val); }' $(ENV_FILE)

install_dependencies:
	pip install uv

install_1:
	uv pip install -e 1_First_NAT_Workflow

validate_1:
	nat validate --config_file 1_First_NAT_Workflow/src/configs/config.yml

run_1_1:
	nat run --config_file 1_First_NAT_Workflow/src/configs/config.yml --input "What is the difference between weather and climate?"

run_1_2:
	nat run --config_file 1_First_NAT_Workflow/src/configs/config.yml --input "How much has global average temperature increased since pre-industrial times?"

run_1_3:
	nat run --config_file 1_First_NAT_Workflow/src/configs/config.yml --input "What were the exact temperature anomalies for the top 5 warmest countries in 2023?"

serve_1:
	nat serve --config_file 1_First_NAT_Workflow/src/configs/config.yml

test_api_1:
	pytest -s 1_First_NAT_Workflow/tests/integration_tests/test_api.py