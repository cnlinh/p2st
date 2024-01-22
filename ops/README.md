# Setting Up from Scratch

1. Update system packages: 
```
sudo apt update
```
3. Install Docker: https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository
4. Install python 3.10
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10
```
5. Install psql to interact with the postgres database: 
```
sudo apt install postgresql-client
```
6. Deploy postgres:
```
cd /home/sadm/chat-gpt/backend
POSTGRES_DB='friday' POSTGRES_USER='friday' POSTGRES_PASSWORD='46104324a6648790d8a4' sudo docker compose up -d
```
Note: This is not vanilla postgres, this is postgres with support for the pgvector extension (https://github.com/pgvector/pgvector?tab=readme-ov-file#docker)

7. Deploy Server:
```
source env/bin/activate
pip install -r requirements.txt
python -m pip install daphne

# copy paste Appendix 1 to the bottom of /etc/supervisord.conf
supervisorctl restart
supervisorctl start backend:
```

8. To check the status:
```
sudo supervisorctl status all
```
