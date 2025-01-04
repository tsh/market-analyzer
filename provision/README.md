Usage:
> `ansible-playbook -i inventory.ini playbook.yaml`

### Prefect worker
Prefect worker requires sudo privileges:
> `ansible-playbook -i inventory.ini prefect_worker.yaml --ask-become-pass`
Note: set up `PREFECT_API_KEY` for some machines

Check status:
> `systemctl list-unit-files | grep prefect`

Logs:
> `journalctl -u prefect_worker.service --follow`