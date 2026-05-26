#!/bin/sh

# COLORS
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'


echo -e "${YELLOW}Attente de Kibana...${RESET}";


limit=0
until curl -s http://kibana:5601/kibana/api/status | grep '"level":"available"';
  do sleep 5;
  echo -e "${CYAN}Tentative $limit/10... En attente des plugins...${RESET}"
  limit=$(( limit + 1))
  if [ "$limit" -eq 10 ]; then
    echo -e "${RED}Kibana n'est pas prêt !${RESET}";
    exit 1;
  fi
done;



echo -e "${GREEN}Kibana est prêt ! Importation des dashboards...${RESET}";

curl -X POST http://kibana:5601/kibana/api/saved_objects/_import?overwrite=true \
  -H 'kbn-xsrf: true' \
  --form file=@/tmp/dashboards.ndjson
