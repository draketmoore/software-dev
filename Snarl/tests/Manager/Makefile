# diff <(jq -S . A.json) <(jq -S . B.json)
all:
	@cp ../../Game/*.py .
clean:
	@rm -rf __pycache__/ *.py
test: all
	@cp ../autoTest.py .
	@echo "Testing current directory"
	@python3 autoTest.py
	@echo "Testing tests/ directory"
	@python3 autoTest.py tests/
	@make clean
