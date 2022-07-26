RED='\033[1;31m'
BLUE='\033[1;34m'
GREEN='\033[1;32m'
RESET='\033[0m'
MY_PROJECT_PATH='/home/zeynix/Python/YoutuBot v0.1/program/main.py'

for i in 1 2 3;
do
	echo -e "${BLUE}────────────────────────────────────────────────────(${RED} START #$i ${BLUE})──────────────────────────────────────────────────── ${RESET}";
	python3 "${MY_PROJECT_PATH}" --game VALORANT;
	echo -e "${BLUE}────────────────────────────────────────────────────(${GREEN}  END #$i  ${BLUE})──────────────────────────────────────────────────── ${RESET}\n";
done;
