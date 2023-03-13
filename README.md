# ContainersJugglers
Creates a few docker containers with ansible and sends file from one to another

# Ansible 

`ansible-playbook run_all.yaml -e "jugglers_number=1" -v`


# Docker
`docker build -t container_1 .`

`docker run --name container_1 -p 5000:5000 -d container`

`uvicorn main:app --reload --port 5000 --host localhost`

`docker rm -f container`
