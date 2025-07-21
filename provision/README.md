### Prefect worker
1. Install prefect workers. Prefect worker requires to run with sudo privileges:
> `ansible-playbook -i inventory.ini prefect_worker.yaml --ask-become-pass`

2. Download selenium drivers
> `ansible-playbook -i inventory.ini selenium_drivers.yaml`
 
IMPORTANT: 
- Environment variable e.g. `TG_TOGEN` are passed on from the host machine when service file is generated
- set up `PREFECT_API_KEY` for some machines

#### Cheat sheet:
Check status:
> systemctl list-unit-files | grep prefect

Logs:
> journalctl -u prefect_worker.service --follow

Check env variables in process
> systemctl status prefect_worker.service
> sudo strings /proc/<Main PID>/environ