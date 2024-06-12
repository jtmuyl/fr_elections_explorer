include .env
PYTHON=$(PYTHON_PATH)
PIP=$(PYTHON_PATH) -m pip


make init:
	-mkdir data
	-mkdir data/election_data
	-mkdir data/election_data/raw
	-mkdir data/election_data/processed
	-mkdir data/geo_data
	-mkdir data/insee_data
	$(PIP) install -r requirements.txt

make download-data: download-election-data download-geo-data

download-election-data:
	# these urls are supposed to be stable
	wget https://www.data.gouv.fr/fr/datasets/r/79b5cac4-4957-486b-bbda-322d80868224 -O data/election_data/raw/presidentielle_2022_t1_burvot.txt
	wget https://www.data.gouv.fr/fr/datasets/r/4dfd05a9-094e-4043-8a19-43b6b6bbe086 -O data/election_data/raw/presidentielle_2022_t2_burvot.txt
	wget https://www.data.gouv.fr/fr/datasets/r/8fdb0926-ea9d-4fb4-a136-7767cd97e30b -O data/election_data/raw/presidentielle_2017_t1_burvot.txt
	wget https://www.data.gouv.fr/fr/datasets/r/2e3e44de-e584-4aa2-8148-670daf5617e1 -O data/election_data/raw/presidentielle_2017_t2_burvot.txt
	wget https://www.data.gouv.fr/fr/datasets/r/a1f73b85-8194-44f4-a2b7-c343edb47d32 -O data/election_data/raw/legislatives_2022_t1_burvot.txt
	wget https://www.data.gouv.fr/fr/datasets/r/cada247a-6528-44e7-8308-30c0c335a4b2 -O data/election_data/raw/legislatives_2022_t2_burvot.txt
	wget https://www.data.gouv.fr/fr/datasets/r/77c4450b-7fa7-425c-84da-4f7bf4b97820 -O data/election_data/raw/europeennes_2019_t1_burvot.txt
	wget https://www.data.gouv.fr/fr/datasets/r/937bb638-a487-40cd-9a0b-610d539a4207 -O data/election_data/raw/europeennes_2024_t1_burvot.txt
download-geo-data:
	# source : https://www.data.gouv.fr/fr/datasets/reconstruction-automatique-de-la-geometrie-des-bureaux-de-vote-depuis-insee-reu-et-openstreetmap/
	wget https://www.data.gouv.fr/fr/datasets/r/d2392385-c12f-4b1b-8940-37da09be6333 -O data/geo_data/bureau-de-vote-insee-reu-openstreetmap.gpkg

preprocess-raw-files:
	$(PYTHON) fr_election_explorer/preprocess_raw_files.py