import clickhouse_connect
import environ
import os

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


def execute_query(query, name):
    client = clickhouse_connect.get_client(host=os.environ.get('CL_DB_HOST')
                         , database=os.environ.get('CL_SCHEMA')
                         , user=os.environ.get('CL_USER')
                         , password=os.environ.get('CL_PASSWORD'))
    # Open and read the file as a single buffer
    fd = open(query, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    cnt = 0
    # Execute every command from the input file
    for command in sqlCommands:
        cnt = cnt + 1
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            client.query(query=command)
            print("successful executed " + name + " command " + str(cnt))
        except OperationalError(msg):
            print(command)
            print("Command skipped: ", msg)