#!/bin/bash
init_datadir() {
	echo "Initializing Postgres data dir..."
	if [[ -d ${PG_DATA_VOLUME} ]]; then
		# Do only if told explicitly: copies files into the persistence filesystem. (Use with caution)
		if [[ ${IS_CLEAN_ENV} == true ]]; then
			echo "Clean environment. Copying to mounted volume..."
			if [ "$(ls -A ${PG_DATA_VOLUME} 2>/dev/null)" ]; then
				echo "Host folder not empty. Skipping copy..."
			else
				echo "Copying ${PG_DATADIR} to ${PG_DATA_VOLUME}"
				cp -R ${PG_DATADIR}/* ${PG_DATA_VOLUME}			
			fi
		else
			echo "Existing environment, not copying anything to mounted volume..."
		fi
	
		echo "Changing permissions of all files in ${PG_DATA_VOLUME} to 0600"
		find ${PG_DATA_VOLUME} -type f -exec chmod 0600 {} \;
		echo "Changing permissions of all folders in ${PG_DATA_VOLUME} to 0700"
		find ${PG_DATA_VOLUME} -type d -exec chmod 0700 {} \;
		echo "Changing ownership of ${PG_DATA_VOLUME} to postgres"
		chown -R postgres:postgres ${PG_DATA_VOLUME}
	else
		echo "!!! Data volume does not exist !!!"
		exit 1
	fi
}

init_configdir() {
	echo "Initializing Postgres config dir..."
	if [[ -d ${PG_CONFIG_VOLUME} ]]; then
		echo "Copying and overwriting ${PG_CONFIGDIR} to ${PG_CONFIGFILE_VOLUME}"
		cp -f ${PG_CONFIGFILE} ${PG_CONFIGFILE_VOLUME}
		echo "Removing ${PG_CONFIGFILE}"
		rm -f ${PG_CONFIGFILE}
			
		echo "Setting ownership and permissions on ${PG_CONFIGDIR}"
		chown -R postgres:postgres ${PG_CONFIG_VOLUME}
		chown root:root ${PG_CONFIGFILE_VOLUME}
        # chown root:root ${PG_CONFIG_VOLUME}/pg_hba.conf
		chmod 666 ${PG_CONFIGFILE_VOLUME}
		# chmod 666 ${PG_CONFIG_VOLUME}/pg_hba.conf
	else
		echo "!!! Config volume does not exist !!!"
		exit 1
	fi
}

init_logdir() {
	echo "Initializing Postgres log dir..."
	if [[ -d ${PG_LOG_VOLUME} ]]; then
		echo "Changing permissions of all files and folders in ${PG_LOG_VOLUME} to 1775"
		chmod -R 1775 ${PG_LOG_VOLUME}
		echo "Changing ownership of ${PG_LOG_VOLUME} to root:postgres"
		chown -R root:postgres ${PG_LOG_VOLUME}
	else
		echo "!!! Log volume does not exist !!!"
		exit 1
	fi
}

set_password() {
	echo "Setting database password for user postgres"
	start_postgres_internally &&\
	psql -U postgres -d postgres -c "ALTER USER postgres with encrypted password '${PG_PASSWORD}';" &&\
	stop_postgres
}

check_env_variables() {
	if [[ -z ${PG_PASSWORD} ]]; then
        echo "ERROR! Please specify a password for postgres in PG_PASSWORD. Exiting..."
        exit 1
	fi
}

exec_as_postgres() {
	sudo -HEu postgres "$@"
}

set_postgresql_param() {
	local key=${1}
	local value=${2}
	local verbosity=${3:-verbose}
	if [[ -n ${value} ]]; then
		local current=$(exec_as_postgres sed -n -e "s/^\(${key} = '\)\([^ ']*\)\(.*\)$/\2/p" ${PG_CONFIGFILE_VOLUME})
		if [[ "${current}" != "${value}" ]]; then
			if [[ ${verbosity} == verbose ]]; then
				echo "Setting ${PG_CONFIGFILE_VOLUME} parameter: ${key} = '${value}'"
			fi
			value="$(echo "${value}" | sed 's|[&]|\\&|g')"
			exec_as_postgres sed -i "s|^[#]*[ ]*${key} = .*|${key} = '${value}'|" ${PG_CONFIGFILE_VOLUME}
		fi
	fi
}

start_postgres() {
	echo "*** Starting PostgreSQL ${PG_VERSION}... ***"
	exec start-stop-daemon --start --chuid postgres:postgres \
		--exec ${PG_BINDIR}/postgres -- \
			-D ${PG_CONFIG_VOLUME}
}

start_postgres_internally() {
	echo "Starting postgres server for internal configuration..."
	rm -rf ${PG_DATA_VOLUME}/postmaster.pid
	set_postgresql_param "listen_addresses" "127.0.0.1" quiet
	exec_as_postgres ${PG_BINDIR}/pg_ctl -D ${PG_CONFIG_VOLUME} -w start
}

stop_postgres() {
	echo "Stopping postgres server after internal configuration..."
	exec_as_postgres ${PG_BINDIR}/pg_ctl -D ${PG_CONFIG_VOLUME} -w stop
	# listen on all interfaces
	set_postgresql_param "listen_addresses" "*" quiet
}

### Starting point ### 

echo "*** Initializing Postgresql ***"

check_env_variables
init_datadir
init_configdir
init_logdir
set_postgresql_param "data_directory" "${PG_DATA_VOLUME}"
set_password

start_postgres