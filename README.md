# ContainersJugglers
![alt text](data/DockerContainersJunggle_logo.png)

Creates **n** docker containers with ansible and sends file ball.yaml from one to another.

## To run the project:

### To deploy the project run this command from project root:

`ansible-playbook run_all.yaml -e "jugglers_number=5" -v`

### Console for running and controlling the process in swagger:

To access exposed APIs of containers:
* **Container_1**: http://localhost:5001/docs
* **Container_2**: http://localhost:5002/docs  
  ...
* **Container_n**: [http://localhost:5000+n/docs]()

### Some explanations:

* In the beginning **container_1** has the ball with counter = 0.
* Start process with `start_juggle` endpoint.
* Stop process with `stop_juggle` endpoint.
* Use `do_i_have_a_ball` endpoint to check count of ball moves from one container to another.
* Juggling stops when you run `stop_juggle` endpoint and ball arrives to the container from which you ran this endpoint.
* While system is juggling you can't get number of ball moves from any containers - you simply won't be able to catch the ball before it's gonna be juggled further.