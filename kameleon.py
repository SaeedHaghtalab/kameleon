__author__ = "Ricardo Fernandes (ricardo.fernandes@esss.se)"
__contributor__ = "Han Lee (han.lee@esss.se)"
__copyright__ = "(C) 2015-2016 European Spallation Source (ESS)"
__license__ = "LGPL3"
__version__ = "1.1.1"
__date__ = "2016/JAN/25"
__description__ = "Kameleon, a behavior-rich and time-aware generic simulator. This simulator, or more precisely server, receives/sends commands/statuses from/to clients through the TCP/IP protocol."
__status__ = "Production"


# ============================
#  IMPORT PACKAGES
# ============================
import sys
import os
import math
import socket
import random
import datetime
import time
import thread
import traceback


# ============================
#  GLOBAL VARIABLES
# ============================
_COMMANDS = []
_STATUSES = []
_CONNECTION = None
_TIMEOUT = 10.0
_QUIET = False
COMMAND_RECEIVED = ""
TERMINATOR = ""
LF = "\n"
CR = "\r"
FIXED = 0
ENUM = 1
INCR = 2
RANDOM = 3
CUSTOM = 4


# ============================
#  FUNCTION THAT SERVES INCOMING REQUESTS
# ============================
def start_serving(port, config_file):
	global _CONNECTION
	global _STATUSES
	global COMMAND_RECEIVED

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	while True:
		try:
			server_socket.bind(("", port))
			break
		except:
			print_message("Waiting for port '%d' to be released." % port)
			time.sleep(2)

	if config_file is None:
		print_message("Start serving at port '%d'." % port)
	else:
		print_message("Start serving at port '%d' using file '%s' (it contains %d commands and %s statuses)." % (port, config_file, len(_COMMANDS), len(_STATUSES)))

	thread.start_new_thread(process_statuses, ())
	while True:
		server_socket.listen(1)
		connection, _ = server_socket.accept()
		print_message("Client connection opened.")
		_CONNECTION = connection
		while True:
			try:
				COMMAND_RECEIVED = connection.recv(1024)
			except:
				COMMAND_RECEIVED = ""
			if COMMAND_RECEIVED == "":
				_CONNECTION = None
				connection.shutdown()
				connection.close()
				print_message("Client connection closed.")
				break
			flag0 = False
			for element in _COMMANDS:
				description, command, status, wait = element
				if command.startswith("***") is True:
					if command.endswith("***") is True:
						if TERMINATOR == "":
							flag1 = (COMMAND_RECEIVED.find(command[3:-3]) != -1)
						else:
							flag1 = (COMMAND_RECEIVED.find(command[3:-3]) != -1 and COMMAND_RECEIVED.endswith(TERMINATOR))
					else:
						tmp = command[3:] + TERMINATOR
						flag1 = COMMAND_RECEIVED.endswith(tmp)
				else:
					if command.endswith("***") is True:
						if TERMINATOR == "":
							flag1 = COMMAND_RECEIVED.startswith(command[:-3])
						else:
							flag1 = (COMMAND_RECEIVED.startswith(command[:-3]) and COMMAND_RECEIVED.endswith(TERMINATOR))
					else:
						tmp = command + TERMINATOR
						flag1 = (COMMAND_RECEIVED == tmp)
				if flag1:
					flag0 = True
					print_message("Command '%s' (%s) received from client." % (convert_hex(COMMAND_RECEIVED), description))
					if status > 0:
						if wait > 0:
							_STATUSES[status - 1][7] = wait
						else:
							send_status(_STATUSES[status - 1])
			if flag0 is False:
				print_message("Unknown command '%s' received from client." % convert_hex(COMMAND_RECEIVED))


# ============================
#  FUNCTION TO PRINT MESSAGE ALONG WITH A TIMESTAMP
# ============================
def print_message(message):
	if _QUIET is False:
		now = datetime.datetime.now()
		print "[%02d:%02d:%02d] %s" % (now.hour, now.minute, now.second, message)


# ============================
#  FUNCTION TO PROCESS STATUSES THAT HAVE TIMED-OUT
# ============================
def process_statuses():
	while True:
		for element in _STATUSES:
			description, behavior, prefix, suffix, value, timeout, remaining0, remaining1, last_value = element
			if timeout > 0:
				remaining = remaining0 - _TIMEOUT
				if remaining > 0:
					element[6] = remaining
				else:
					element[6] = timeout
					send_status(element)
			if remaining1 > 0:
				remaining = remaining1 - _TIMEOUT
				if remaining > 0:
					element[7] = remaining
				else:
					element[7] = 0
					send_status(element)
		time.sleep(_TIMEOUT / 1000.0)


# ============================
#  FUNCTION TO SEND STATUS TO THE CLIENT
# ============================
def send_status(element):
	description, behavior, prefix, suffix, value, timeout, remaining0, remaining1, last_value = element
	try:
		if behavior == FIXED:
			result = "%s%s%s" % (prefix, value, suffix)

		elif behavior == ENUM:
			if last_value is None:
				if type(value) is list:
					tmp = value[0]
				else:
					tmp = value
			else:
				if type(value) is list:
					try:
						tmp = value[value.index(last_value) + 1]
					except:
						tmp = value[0]
				else:
					tmp = value
			result = "%s%s%s" % (prefix, tmp, suffix)
			element[8] = tmp

		elif behavior == INCR:
			if last_value is None:
				if type(value) is list:
					if int(value[2]) > 0:
						tmp = value[0]
					else:
						tmp = value[1]
				else:
					tmp = "0"
			else:
				if type(value) is list:
					i = int(last_value) + int(value[2])
					if int(value[2]) > 0:
						if i > int(value[1]):
							tmp = value[0]
						else:
							tmp = i
					else:
						if i < int(value[0]):
							tmp = value[1]
						else:
							tmp = i
				else:
					tmp = int(last_value) + int(value)
			result = "%s%s%s" % (prefix, tmp, suffix)
			element[8] = tmp

		elif behavior == RANDOM:
			if type(value) is list:
				i = int(value[0])
				j = int(value[1])
				if i > j or (i == 0 and j == 0):
					result = "%s0%s" % (prefix, suffix)
				else:
					result = "%s%s%s" % (prefix, random.randrange(i, j + 1), suffix)
			else:
				i = int(value)
				if i == 0:
					result = "%s0%s" % (prefix, suffix)
				elif i > 0:
					result = "%s%s%s" % (prefix, random.randrange(0, i + 1), suffix)
				else:
					result = "%s%s%s" % (prefix, random.randrange(i, 1), suffix)

		elif behavior == CUSTOM:
			result = "%s%s%s" % (prefix, eval(value), suffix)

		else:
			result = ""
	except Exception as e:
		print e
		result = ""
	try:
		tmp = result + TERMINATOR
		_CONNECTION.sendall(tmp)
		print_message("Status '%s' (%s) sent to client." % (convert_hex(tmp), description))
	except:
		pass   # no need to print the exception as most probably it is due to the connection be closed in the meantime


# ============================
#  FUNCTION TO CONVERT CHARs BELOW 32 INTO A TEXTUAL REPRESENTATION
# ============================
def convert_hex(text):
	result = ""
	for c in text:
		if ord(c) < 32:
			result = "%s<%s>" % (result, format(ord(c), "#04x"))
		else:
			result = "%s%s" % (result, c)
	return result


# ============================
#  FUNCTION TO SHOW THE HEADER OF THE TOOL
# ============================
def show_header():
	tmp = "Kameleon v%s (%s - %s)" % (__version__, __date__, __status__)
	i = len(__copyright__)
	print
	print "*" * (i + 6)
	print "*  %s  *" % (" " * i)
	print "*  %s %s *" % (tmp, " " * (i - len(tmp)))
	print "*  %s  *" % (" " * i)
	print "*  %s  *" % (" " * i)
	print "*  %s  *" % __copyright__
	print "*  %s  *" % (" " * i)
	print "*" * (i + 6)
	print


# ============================
#  MAIN PROGRAM
# ============================
if __name__ == "__main__":


	# ============================
	#  DEFAULT VALUES
	# ============================
	port = 9999
	config_file = None


	# ============================
	#  PROCESS ARGUMENTS
	# ============================
	terminator = None
	for argument in sys.argv[1:]:
		if argument.upper() == "--HELP":
			show_header()
			print "  --help          Show this help."
			print
			print "  --quiet         Do not show info messages when running."
			print
			print "  --port=X        Serve at port 'X'. If not specified, default port is '%d'." % port
			print
			print "  --file=X        Use file 'X' which describes the commands/statuses to"
			print "                  receive/send from/to clients."
			print
			print "  --terminator=X  Define 'X' as the terminator of the commands/statuses. It can"
			print "                  either be an arbitrary string (e.g. 'END') or one of the"
			print "                  following pre-defined terminators:"
			print "                     LF   : line feed (0xA)"
			print "                     CR   : carriage return (0xD)"
			print "                     LF+CR: line feed (0xA) followed by a carriage return (0xD)"
			print "                     CR+LF: carriage return (0xD) followed by a line feed (0xA)"
			print
			sys.exit(0)

		elif argument.upper() == "--QUIET":
			_QUIET = True

		elif argument[:7].upper() == "--PORT=":
			tmp = argument[7:].strip()
			if tmp == "":
				print "Please specify the port number."
				print
				sys.exit(-1)
			else:
				try:
					port = int(tmp)
				except:
					print "Port '%s' invalid." % tmp
					print
					sys.exit(-1)

		elif argument[:7].upper() == "--FILE=":
			config_file = argument[7:].strip()
			if config_file == "":
				print "Please specify the file that describes the commands/statuses to receive/send from/to clients."
				print
				sys.exit(-1)
			try:
				handler = open(config_file, "rb")
				content = handler.read()
				handler.close()
			except:
				print "Error when reading file '%s'." % config_file
				print
				sys.exit(-1)
			try:
				exec(content)
			except Exception as e:
				_, _, trace_back = sys.exc_info()
				print "Error when processing line '%d' in file '%s' (description: %s)." % (traceback.extract_tb(trace_back)[-1][1], config_file, e)
				print
				sys.exit(-1)
			try:
				count = 0
				for element in STATUSES:
					count = count + 1
					i = len(element)
					if i == 3:
						description, behavior, value = element
						prefix = ""
						suffix = ""
						timeout = 0
						flag = True
					elif i == 4:
						description, behavior, value, prefix = element
						suffix = ""
						timeout = 0
						flag = True
					elif i == 5:
						description, behavior, value, prefix, suffix = element
						timeout = 0
						flag = True
					elif i == 6:
						description, behavior, value, prefix, suffix, timeout = element
						flag = True
					else:
						flag = False
					if flag is True:
						_STATUSES.append([description, behavior, prefix, suffix, value, timeout, 0, 0, None])
					else:
						print "The status #%d in list 'STATUSES' has an incorrect form." % count
			except:
				print "The list 'STATUSES' is missing in file '%s' or its form incorrect." % config_file
			try:
				count = 0
				for element in COMMANDS:
					count = count + 1
					i = len(element)
					if i == 2:
						description, command = element
						status = 0
						wait = 0
						flag = True
					elif i == 3:
						description, command, status = element
						wait = 0
						flag = True
					elif i == 4:
						description, command, status, wait = element
						flag = True
					else:
						flag = False
					if flag is True:
						if status >= 0 and status <= len(_STATUSES):
							_COMMANDS.append([description, command, status, wait])
						else:
							print "The command '%s' in list 'COMMANDS' points to status #%d which does not exist in list 'STATUSES'." % (description, status)
							_COMMANDS.append([description, command, 0, wait])
					else:
							print "The command #%d in list 'COMMANDS' has an incorrect form." % count
			except:
				print "The list 'COMMANDS' is missing in file '%s' or its form incorrect." % config_file

		elif argument[:13].upper() == "--TERMINATOR=":
			terminator = argument[13:]

		else:
			print "Parameter '%s' invalid. Please execute with '--help' to see valid parameters." % argument
			print
			sys.exit(-1)


	# ============================
	#  SETUP TERMINATOR DEFINED THROUGH THE PARAMETER (THE TERMINATOR DEFINED IN THE TEMPLATE FILE WILL BE OVERWRITTEN)
	# ============================
	if terminator is None:
		TERMINATOR = str(TERMINATOR)
	else:
		tmp = terminator.replace(" ", "").upper()
		if tmp == "LF":
			TERMINATOR = LF
		elif tmp == "CR":
			TERMINATOR = CR
		elif tmp == "LF+CR":
			TERMINATOR = LF + CR
		elif tmp == "CR+LF":
			TERMINATOR = CR + LF
		else:
			TERMINATOR = terminator


	# ============================
	#  START SERVING
	# ============================
	if _QUIET is False:
		show_header()
	try:
		start_serving(port, config_file)
		sys.exit(0)
	except KeyboardInterrupt:
		print_message("Stop serving due to user request.")
		sys.exit(0)
	except Exception as e:
		print_message("Stop serving due to an error (description: %s)." % e)
		sys.exit(-1)
