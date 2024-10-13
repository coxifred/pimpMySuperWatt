DB_URL="http://localhost:8086"
DB="pimpMySuperWatt"

curl -G "${DB_URL}/query?pretty=true" --data-urlencode "db=${DB}" --data-urlencode "q=delete from ${DB}"
