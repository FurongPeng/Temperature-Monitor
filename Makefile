install:
	(cd CH341SER_LINUX  && make  && make load)
	chmod +x t-monitor
	cp t-monitor /etc/init.d/
	if [ ! -d "/usr/local/t-monitor" ] ; then mkdir /usr/local/t-monitor; fi
	cp t-monitor.sh /usr/local/t-monitor/
	cp email.cfg /usr/local/t-monitor/
	cp Sendmail.py /usr/local/t-monitor/

	-/sbin/chkconfig --add t-monitor
	-/sbin/chkconfig t-monitor on
	service t-monitor start

clean:
	service t-monitor stop
	-/sbin/chkconfig t-monitor off
	-/sbin/chkconfig -d t-monitor
	-(cd CH341SER_LINUX  && make unload  && make clean)
	if [ -d /usr/local/t-monitor ] ; then rm -rf /usr/local/t-monitor ; fi
	if [ -f /usr/init.d/t-monitor ] ; then rm  /usr/init.d/t-monitor ; fi
