
sudo docker-compose build
sudo docker-compose rm -f elk_mongo ||echo "no elk_mongo"
sudo docker-compose up -d