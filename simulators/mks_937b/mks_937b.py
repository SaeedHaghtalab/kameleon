# author: Nawzad Al habib
# email: nawzadalhabib@esss.se
# copyright: (C) 2017 European Spallation Source (ESS)
# version: 1.0.0
# date: 2017/JUN/26
# description: Kameleon simulator file for the MKS 937B (vacuum gauge controller)



# The terminator (EOL) of commands/statuses is described in the "TERMINATOR" variable. By default, the terminator is not defined (i.e. is empty). If defined, the terminator is inserted at the end of both the commands and statuses received/sent from/to clients before Kameleon starts to process these. The generic form of this variable is:
#
#    TERMINATOR = value
#
# Where value can either be an arbitrary string (e.g. "END") or one of the following pre-defined terminators:
#
#    LF     : the terminator is a line feed (0xA).
#    CR     : the terminator is a carriage return (0xD).
#    LF + CR: the terminator is a line feed (0xA) followed by a carriage return (0xD).
#    CR + LF: the terminator is a carriage return (0xD) followed by a line feed (0xA).
#
# In case of need to setup different terminators for commands and statuses, the "TERMINATOR_CMD" and "TERMINATOR_STS" variables can be used respectively (e.g. TERMINATOR_CMD = LF).

TERMINATOR = CR + LF



# Data (i.e. commands) received from the client are described in the "COMMANDS" list. The generic form of this list is:
#
#    COMMANDS = [[description_1, command_1, status_1, wait_1], [description_2, command_2, status_2, wait_2], ..., [description_X, command_X, status_X, wait_X]]
#
# Where:
#
#    description: (mandatory) string that describes the command (e.g. "Set power on").
#    command    : (mandatory) string that represents the command (e.g. "AC1"). Only data (received from the client) that matches exactly the command is selected. Additional matching policies are available:
#                    - if command starts with "***", any data (received from the client) that ends with command is selected.
#                    - if command ends with "***", any data (received from the client) that starts with command is selected.
#                    - if command starts and ends with "***", any data (received from the client) that contains the command is selected.
#    status     : (optional) integer, list or string that specifies the index(es) of the status(es) (stored in the "STATUSES" list) to send to the client or a user-defined function (to be called by Kameleon) after the command is selected. The first status (stored in "STATUSES" list) is at index 1. If 0 or not specified, no status is sent.
#    wait       : (optional) integer that specifies the time to wait (in milliseconds) before sending the status to the client. If 0 or not specified, the status is immediately sent (i.e. right after the command is received).


#.              COMMANDS                                                          DISCRIPTION
#              @254CPn!ON;FF                                       n=1 to 6 , Turn on/off the channel power for a sensor (PR/CP/CC/Hc).
#              @254CPn!OFF;FF                                      n=1 to 6 , Turn on/off the channel power for a sensor (PR/CP/CC/Hc).
#              @254DGn!ON;FF.                                      n=1,3,5  , Turn on/off the degas power for a hot cathode gauge.
#              @254DGn!OFF;FF.                                     n=1,3,5  , Turn on/off the degas power for a hot cathode gauge.
#              @254PC1?;FF                                         Qurey the pressure on combined Aout1.
#              @254PC2?;FF                                         Qurey the pressure on combined Aout2.
#              @254SPC1!HH,MM,LL and @254SPC2!HH,MM,LL           set the gauge combination (HH,MM,LL High,Middle, low range pressure gauge)
#              @254PC1?;FF and @254PC1?;FF                           Qurey the gauge combination
#              @254EPC1!Enable;FF and @254EPC1!Disable;FF           Enable/Disable the combined analog output.
#              @003PR1?;FF                                         Qurey the pressure on the channel A1.
#              @001BR!19200;FF                                     To set new baud rate.
#              @003PRn?;FF                                         n=1 to 6, Read the pressure on the chanel n.
#              @004PRZ?;FF                                          Read the pressures on all channel.
#              @254PC1?;FF and @254PC2?;FF                          Read pressure on channel n and its combination
#              @014SPm!3.02E-3;FF                                   m=1 to 12,  set a point for relay m.
#              @015SDm!ABOVE;FF  and @015SDm!BELOW;FF               m=1 to 12, set direction for rely m.
#              @016ENm!SET;FF  and.  @016ENm!ENABLE;FF              m=1 to 12, Qurey or set  status for relay m.
#              @253AD?;FF                                           Qurey or set controller address.
#              @005CAL!Enable;FF                                     Enable/Disable calibration.
#

COMMANDS = [["Turn on channel power","@254CP***!ON;FF",1],
			["Turn on channel power","@254CP***!OFF;FF", 2],
			["Turn on dagas power for a hot cathode gauge","@254DG***!ON;FF",3],
			["Turn off dagas power for a hot cathode gauge","@254DG***!OFF;FF",4],
			["Read the pressure on channel","@003PR***?;FF",5],
			["Read the pressure on all channels","@004PRZ?;FF",6],
			["Read the pressure on combined Aout 1","@254PC1?;FF",7],
			["Read the pressure on combined Aout 2","@254PC2?;FF",8],
			["Disabled the combination Aout 1","@004PC1?FF",9],
			["Disabled the combination Aout 2","@004PC2?FF",10],
			["Set the combination PC1","@254SPC1!HH,MM,LL;FF",11],
			["Set the combination PC2","@254SPC2!HH,MM,LL;FF",12],
			["Qurey the gauge combination","@254SPC1?;FF",13],
			["Qurey the gauge combination","@254SPC2?;FF",14],
			["Enable the combined analog output","@254EPC1!Enable;FF",15],
			["Disable the combined analog output","@254EPC1!Disable;FF",16],
			["Qurey or set controller address","@253AD?;FF",17],
			["Set baud rate","@001BR!9600;FF",18],
			["Set the parity for controller","@002PAR!NONE;FF",19],
			["Enable Disable Calibration","@005CAL!Enable;FF",20],
			["Set the dalay time","@006DLY!8;FF",21],
			["Set the Display mode","@007DM!STD;FF",22],
			[" Enable front panel lock","@008LOCK!ON;FF",23],
			["Disable front panel lock","@008LOCK!OFF;FF",24],
			["Enable parameter setting","@009SPM!Enable;FF",25],
			[" Set the Unite","@010U!Torr;FF",26],
			["Set the type of DAC linear (LIN, V=A*P of logarithmic linear (LOG V=A*LogP+B)","@011DLT***!LOG;FF", 27],
			["Set the DAC slope parameter A.","@012DLA***!0.6;FF",28],
			["Display the sensor module type","@0013MT?;FF",29],
			["Set a setpoint for relay m (m=1 to 12)","@014SP***!3.02E-3;FF",30],
			["Set the direction of relay m to ABOVE", "@015SD***!ABOVE;FF",31],
			["Set the direction of relay m to BELOW","@015SD***!BELOW;FF",32],
			["Set the status for relay m.","@016EN***!SET;FF",33],
			["Set the status for relay m. Response with current Enable status","@016EN***!ENABLE;FF",34],
			["Query relay setpoint status, SET is activeted and CLEAR is disable","@017SS***!SET;FF",35]]




# Data (i.e. statuses) sent to the client are described in the "STATUSES" list. The generic form of this list is:
#
#    STATUSES = [[description_1, behavior_1, value_1, prefix_1, suffix_1, timeout_1], [description_2, behavior_2, value_2, prefix_2, suffix_2, timeout_2]], ..., [description_X, behavior_X, value_X, prefix_X, suffix_X, timeout_X]]
#
# Where:
#
#    description: (mandatory) string that describes the status (e.g. "Get temperature value").
#    behavior   : (mandatory) integer that specifies the behavior for generating the status. It can either be:
#                    - FIXED (sends a fixed value to the client)
#                    - ENUM (sends a value - belonging to an enumeration - to the client)
#                    - INCR (sends an incremented value to the client)
#                    - RANDOM (sends a random value to the client)
#                    - CUSTOM (sends a value from a user-defined function to the client)
#    value      : (mandatory) value to send to the client. Depending on the behavior, it can either be an integer, float, string or list:
#                    - when FIXED, the value is expected to be an integer, float or string. Independently of how many times it is sent to the client, the value remains the same (i.e. does not change).
#                    - when ENUM, the value is expected to be a list. It represents a set of elements (enumeration). After sending an element of the list to the client, the next value to be sent is the next element in the list. When the last element is sent, the next to be sent is the the first element of the list.
#                    - when INCR, the value is expected to be an integer, float or list. If an integer or float, the first value to be sent is a 0 and subsequent values to be sent are incremented by value. If a list, the lower bound, upper bound and increment values are defined by the first, second and third elements of the list, respectively.
#                    - when RANDOM, the value is expected to be an integer or a list. If an integer, a random number between 0 and value is generated. If a list, the lower and upper bounds of the random number to generate are defined by the first and second elements of the list, respectively. The generated random number is sent to the client.
#                    - when CUSTOM, the value is expected to be a string. It contains the name of a user-defined Python function to be called by Kameleon. The value returned by this function is sent to the client (if the function does not return a value or it returns None, nothing is sent).
#    prefix     : (optional) string that contains the prefix to insert at the beginning of the value to send to the client. If not specified, nothing is inserted.
#    suffix     : (optional) string that contains the suffix to insert at the end of the value to send to the client. If not specified, nothing is inserted.
#    timeout    : (optional) integer that specifies the time-out (in milliseconds) after which the status is sent to the client (i.e. time-based). If 0 or not specified, the status is only sent after receiving a command from the client (i.e. event-based).

# Max. Frequency need more invistigation to set the best value.
# Max. frequency for instant is 800, it is between [0,1000], but the user can set any value.
# Critical value is need more invistigation to set the best value.
# Critical frequency is 800, it is between [0,1000], but the user cant set best value.

STATUSES = [["Turn on channel",CUSTOM,"set_ch_on()"],
            ["Turn off channel power",CUSTOM,"set_ch_off()"],
            [ "Turn on dagas power for a hot cathode gauge",CUSTOM,"set_dagas_power_HC_on()"],
            ["Turn off dagas power for a hot cathode gauge",CUSTOM,"set_dagas_power_HC_off()"],
            ["Read the pressure on channel",CUSTOM,"read_pressure()"],
            ["Read the pressure on all channels",CUSTOM,"read_pressure_allchannel()"],
            ["Read the pressure on combined Aout 1",CUSTOM, "read_pressure_comb()"],
            ["Read the pressure on combined Aout 2",CUSTOM, "read_pressure_comb()"],
            ["Disabled the combination Aout 1",FIXED, "@004NAK181;FF"],
            ["Disabled the combination Aout 2",FIXED, "@004NAK181;FF"],
            ["Set the combination PC1",FIXED,"@254ACKNA,NA,NA;FF"],
            ["Set the combination PC1",FIXED,"@254ACKNA,NA,NA;FF"],
            ["Qurey the gauge combination",FIXED,"@254ACK?;FF"],
            ["Qurey the gauge combination",FIXED,"@254ACK?;FF"],
            ["Enable the combined analog output",FIXED, "@254ACKEnable;FF"],
            ["Disable the combined analog output",FIXED,"@254ACKDisable;FF"],
            ["Qurey or set controller address",FIXED,"@253ACK;FF"],
            ["Set baud rate",FIXED,"@001ACK9600;FF"],
            ["Set the parity for controller",FIXED,"@002ACKNONE;FF"],
            ["Enable Disable Calibration",FIXED,"@005ACKEnable;FF"],
            ["Set the dalay time",FIXED,"@006ACK8;FF"],
            ["Set the Display mode",FIXED,"@007ACKSTD;FF"],
            [" Enable front panel lock",FIXED,"@008ACKON;FF"],
            ["Disable front panel lock",FIXED,"@008ACKOFF;FF"],
            ["Enable parameter setting",FIXED,"@009ACKEnable;FF"],
            ["Set the unite", FIXED,"@010ACKTorr;FF"],
            ["Set the type of DAC linear (LIN, V=A*P of logarithmic linear (LOG V=A*LogP+B)",CUSTOM,"set_dac_Line()"],
            ["Set the DAC slope parameter A",CUSTOM,"set_dac_slop_para()"],
            ["Display the sensor module type",CUSTOM,"disp_sensor_typy()"],
            ["Set a setpoint for relay m (m=1 to 12)",CUSTOM,"set_relay()"],
            ["Set the direction of relay m to ABOVE",CUSTOM,"set_dir_relay_Above()"],
            ["Set the direction of relay m to BELOW",CUSTOM,"set_dir_relay_Below()"],
            ["Set the status for relay m.",CUSTOM,"set_relay_stat_set()"],
            ["Set the status for relay m. Response with current Enable status",CUSTOM,"set_relay_stat_enable()"],
            ["Query relay setpoint status, SET is activeted and CLEAR is disable",CUSTOM,"relay_setpoint_status()"]]




#SP=["@254CP1!ON;FF",  "@254CP2!ON;FF",  "@254CP3!ON;FF", "@254CP4!ON;FF", "@254CP5!ON;FF" ,"@254CP6!ON;FF"]
#CH_ON = ["@002ACKON;FF", "@002ACKON;FF", "@002ACKON;FF", "@002ACKON;FF", "@002ACKON;FF", "@002ACKON;FF"]
Is_ch_on = [0,0,0,0,0,0]	#0 = off, 1 = on
Is_ch_off= [1,1,1,1,1,1]


chn=0
def set_ch_on():


	data= COMMAND_RECEIVED.split("P")

	data = data[1].split("!")

	#print data
	ch=int(data[0])-1
	chk=['A1','A2','B1','B2','C1','C2']
	print  'Channel Number {}  is now ON corresponding to the gauge connected to channel {}'.format(ch+1,chk[ch])


	Is_ch_on[ch] = 1
	#print Is_ch_on


  	return "@002ACKON;FF"

def set_ch_off():

	data= COMMAND_RECEIVED.split("P")

	data = data[1].split("!")

	#print data
	ch=int(data[0])-1
	chk=['A1','A2','B1','B2','C1','C2']
	print  'Channel Number {}  is now OFF corresponding to the gauge connected to channel {}'.format(ch+1,chk[ch])
	#print ch

	Is_ch_off[ch] = 0
	 #print Is_ch_off


  	return "@002ACKOFF;FF"


def set_dagas_power_HC_on():

	data= COMMAND_RECEIVED.split("G")
	data = data[1].split("!")

	#print data
	ch=int(data[0])-1
	ch_n=[1,3,5]
	cnk=['A1','B1','C1']


	if (ch+1) in ch_n:

		print  'The degas power is On for the hot cathode gauge, the channel Number {} '.format(ch+1)
		return "@002ACKON;FF"

	else:
		 print "The channel number must be 1 for A1 ,3 for B1 or 5 for C1"


def set_dagas_power_HC_off():

	data= COMMAND_RECEIVED.split("G")
	data = data[1].split("!")

	ch=int(data[0])-1
   	ch_n=[1,3,5]

	if (ch+1) in ch_n:

			print  'The degas power is OFF for the hot cathode gauge, the channel Number {} '.format(ch+1)

			return "@002ACKOFF;FF"

	else:
			print "The channel number must be 1 for A1 ,3 for B1 or 5 for C1."

def read_pressure():
	data= COMMAND_RECEIVED.split("R")
	data = data[1].split("?")

	ch=int(data[0])-1
	print  'Read the  pressure on the Channel Number {}  '.format((ch+1))




	return "@003ACK7.602E+2;FF"



def read_pressure_comb():
	data= COMMAND_RECEIVED.split("C")
	data = data[1].split("?")
	ch=int(data[0])-1
	chn=[1,2]

	print  'Channel Number and its combination  is {}'.format(ch+1)

	if (ch+1) in chn:
		return "@254ACK7.602E+2;FF"
	else:
		print "The channel number must be 1 or 2"


def read_pressure_allchannel():

	return "@004ACK7.602E+2;FF" "@004ACK7.602E+2;FF" "@004ACK7.602E+2;FF" "@004ACK7.602E+2;FF" "@004ACK7.602E+2;FF" "@004ACK7.602E+2;FF"




def set_dac_Line():

	data= COMMAND_RECEIVED.split("T")
	data = data[1].split("L")
	return "@011ACKLOG;FF"


def set_dac_slop_para():
		data= COMMAND_RECEIVED.split("A")
		data = data[1].split("!")

	 	return  "@011ACK0.6;FF"

def disp_sensor_typy():

	#sensortstypes=[ 'T1,T2,T3,T4]

	T1=['CC','HC','CM','PR','NC']

	print 'The sensors type connected is {}'.format(T1)
	return "@0013ACKT1?;FF"

def set_relay():
		data= COMMAND_RECEIVED.split("P")
		data = data[1].split("!")

    		return "@0014ACK3.02E-3;FF"


def set_dir_relay_Above():
		data= COMMAND_RECEIVED.split("D")
		data = data[1].split("!")


		return "@015ACKABOVE;FF"

def set_dir_relay_Below():
		data= COMMAND_RECEIVED.split("D")
		data = data[1].split("!")

		return "@015ACKNAK162;FF"

def set_relay_stat_set():

		data= COMMAND_RECEIVED.split("N")
		data = data[1].split("!")
		return "@016ACKSET;FF"

def set_relay_stat_enable():

		data= COMMAND_RECEIVED.split("N")
		data = data[1].split("!")
		return "@016ACKENABLE;FF"


def relay_setpoint_status():

  		data= COMMAND_RECEIVED.split("S")
		data = data[1].split("!")
 		return "@017ACKSET?;FF"
