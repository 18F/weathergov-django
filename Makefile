zap: zap-containers containers-up pause import-spatial load-spatial
rezap: dump-spatial zap

import-spatial:
ifneq ("weather.gov/spatial-data/dump.mysql","")
	cat weather.gov/spatial-data/dump.mysql | docker compose exec -T database mysql -udrupal -pdrupal -hdatabase weathergov
endif

### Spatial data
load-spatial: # Load spatial data into the database
	docker compose run --rm spatial node load-shapefiles.js

dump-spatial:
	docker compose exec database mysqldump -udrupal -pdrupal -hdatabase --no-tablespaces weathergov weathergov_geo_metadata weathergov_geo_states weathergov_geo_counties weathergov_geo_places weathergov_geo_cwas weathergov_geo_zones > weather.gov/spatial-data/dump.mysql

update-settings:
	cp -f weather.gov/web/sites/example.settings.dev.php weather.gov/web/sites/settings.dev.php

zap-containers:
	docker compose stop
	docker compose rm -f

containers-up:
	docker compose up -d

pause:
	sleep 15

build-css: # Build CSS
	docker compose run --rm uswds npx gulp compile

python-lint:
	docker compose exec web python -m black .
