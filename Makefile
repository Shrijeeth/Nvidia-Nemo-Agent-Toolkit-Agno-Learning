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
	$(if $(wildcard $(ENV_FILE)),@:, $(error [env] missing $(ENV_FILE)))

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
	@powershell -NoProfile -ExecutionPolicy Bypass -File "$(CURDIR)/scripts/export_env_pwsh.ps1" -EnvFile "$(ENV_FILE)"

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
	uv pip install -e 1_Climate_Agent_Workflow

validate_1:
	nat validate --config_file 1_Climate_Agent_Workflow/src/configs/config.yml

run_1_1:
	nat run --config_file 1_Climate_Agent_Workflow/src/configs/config.yml --input "What is the difference between weather and climate?"

run_1_2:
	nat run --config_file 1_Climate_Agent_Workflow/src/configs/config.yml --input "How much has global average temperature increased since pre-industrial times?"

run_1_3:
	nat run --config_file 1_Climate_Agent_Workflow/src/configs/config.yml --input "What were the exact temperature anomalies for the top 5 warmest countries in 2023?"

run_1_4:
	nat run --config_file 1_Climate_Agent_Workflow/src/configs/config.yml --input "What is the global temperature trend per decade?"

run_1_5:
	nat run --config_file 1_Climate_Agent_Workflow/src/configs/config.yml --input "Compare the temperature trends of Canada and Brazil. Which one is warming faster? Also create a visualization of global trends."

run_1_6:
	nat run --config_file 1_Climate_Agent_Workflow/src/configs/config.yml --input "Create a visualization showing which countries have the highest warming trends."

run_1_7:
	nat run --config_file 1_Climate_Agent_Workflow/src/configs/config.yml --input "What is the global temperature trend per decade?"

run_1_8:
	nat run --config_file 1_Climate_Agent_Workflow/src/configs/config.yml --input "Tell me about France's climate data. How many stations does it have and what's the temperature trend?"

run_1_9:
	nat run --config_file 1_Climate_Agent_Workflow/src/configs/config.yml --input "A country's emissions were 1,200 Mt in 2015. They reduced emissions by 2.5% annually until 2020, then accelerated reductions to 4% annually. What are the emissions in 2025?"

run_1_10:
	nat run --config_file 1_Climate_Agent_Workflow/src/configs/config.yml --input "If temperature rose from 14.2°C to 15.8°C over 43 years, what's the CAGR?"

serve_1:
	nat serve --config_file 1_Climate_Agent_Workflow/src/configs/config.yml

test_api_1:
	pytest -s 1_Climate_Agent_Workflow/tests/integration_tests/test_api.py

eval_1:
	nat eval --config_file 1_Climate_Agent_Workflow/src/configs/config.yml