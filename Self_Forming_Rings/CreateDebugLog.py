import logging

# create  Debug logger
Debuglogger = logging.getLogger('developer_log')
Debuglogger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.FileHandler('network.log')
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%d/%m/%Y %I:%M:%S %p')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
Debuglogger.addHandler(ch)


# create  User logger
Userlogger = logging.getLogger('user_log')
Userlogger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch1 = logging.FileHandler('user.log')
ch1.setLevel(logging.DEBUG)

# create formatter
formatter1 = logging.Formatter('%(message)s','%p')

# add formatter to ch
ch1.setFormatter(formatter1)

# add ch to logger
Userlogger.addHandler(ch1)




