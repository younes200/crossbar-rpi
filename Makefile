default:
	@echo "Targets: start, stop, restart, status, log, install"

start:
	sudo systemctl start robot

stop:
	sudo systemctl stop robot

restart:
	sudo systemctl restart robot

status:
	systemctl status robot

log:
	journalctl -n 100 -f -u robot

install:
	sudo cp robot.service /etc/systemd/system/robot.service
	sudo systemctl daemon-reload
	sudo systemctl enable robot
	sudo systemctl restart robot
