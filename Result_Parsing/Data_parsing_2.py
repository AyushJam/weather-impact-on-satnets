import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def delete_elements(input_list, element): 
    c = input_list.count(element) 
    for i in range(c): 
        input_list.remove(element) 
    return input_list
 
input_path = "./output_logs/case2_thrpt/"
output_path = "./parsed_data/"
output_plots_path = input_path+"plots/"

### Add the name of the files in the directory in the following order: iperf_log_file, ping_log_file, emulator_log_file 
files_list = ["iperf3_log_case2_thrpt.txt", "ping_log_case2_thrpt.txt", "emulator_log_case2_thrpt.txt"]
lines_list = []

### iperf_log parsing
with open(input_path+files_list[0],'r') as file:
    file_content = file.read()
    
lines_list = file_content.split('\n')

splitted_lines_list = []
for line in lines_list:
    words_list = delete_elements(line.split(' '),'')
    splitted_lines_list.append(words_list)
    
time_indices_list_iperf = []
interval_start_list = []
bit_rate_list = []
retransmission_list = []

num = 0
iperf_flag_1 = False
iperf_flag_2 = False
for idx, line in enumerate(splitted_lines_list):
    # print("idx: ",idx)
    ### Assumes that structure of the input file remains same. Might have to be change this otherwise   
    if line.count('-')>20:
        break

    elif ('ID]' in line) and ('Interval' in line):
        iperf_flag_1 = True

    elif iperf_flag_1 and idx<len(splitted_lines_list)-1 and len(splitted_lines_list[idx+1])>9 and float(splitted_lines_list[idx+1][9])==0:
        iperf_flag_2 = True

    if iperf_flag_2 and len(line)>5: 
        # print(line)
        interval_start_list.append(int(float(line[5].split('-')[0])))
        bit_rate_list.append(float(line[9]))
        retransmission_list.append(int(line[11]))
        
# initial_date = int(splitted_lines_list[0][1])
# initial_time_idx = splitted_lines_list[0][2]
# initial_time_h = int(initial_time_idx.split(":")[0])
# initial_time_m = int(initial_time_idx.split(":")[1])
# initial_time_s = int(initial_time_idx.split(":")[2])

# print("interval start list:\n",interval_start_list)

# print('init time ind: ',initial_time_h,"hrs ,",initial_time_m,"mins ,",initial_time_s,"secs")

# for i in range(len(interval_start_list)):
#     time_s = initial_time_s+interval_start_list[i]
#     time_m = initial_time_m+int(time_s/60)
#     time_s = time_s%60
#     time_h = initial_time_h+int(time_m/60)
#     time_m = time_m%60
#     curr_date = initial_date + int(time_h/24)
#     time_h = time_h%24
#     if time_s<10:
#         time_s_str = "0"+str(time_s)
#     else:
#         time_s_str = str(time_s)
#     if time_m<10:
#         time_m_str = "0"+str(time_m)
#     else:
#         time_m_str = str(time_m)
#     if time_h<10:
#         time_h_str = "0"+str(time_h)
#     else:
#         time_h_str = str(time_h)
    
#     time_indices_list_iperf.append(time_h_str+":"+time_m_str+":"+time_s_str)

print("####IPerf Data")
for idx, interval in enumerate(interval_start_list):
    print(f"interval: {interval}, bit_rate: {bit_rate_list[idx]}, retransmission: {retransmission_list[idx]}")


### Emulator log parsing
with open(input_path+files_list[2],'r') as file:
    file_content = file.read()
    
lines_list = file_content.split('\n')

splitted_lines_list = []
for line in lines_list:
    words_list = delete_elements(line.split(' '),'')
    splitted_lines_list.append(words_list)
    
time_indices_list_emulator = []
cycle_number_list = []

for idx, line in enumerate(splitted_lines_list):
    if len(cycle_number_list)==len(time_indices_list_emulator):
        if "cycle:" in line:
            cycle_number_list.append(int(line[-1]))

    else:
        if "cycle:" in line:
            cycle_number_list[-1] = int(line[-1])

        if "Time" in line and "Stamp:" in line:
            # if (len(time_indices_list_emulator)>0) and time_indices_list_emulator[-1]==line[-1]:
            #     print(f"cycle: {cycle_number_list[-1]} ALERT!")

            time_indices_list_emulator.append(line[-1])

new_time_indices_list_emulator = []
new_cycle_number_list = []
for idx, time_idx in enumerate(time_indices_list_emulator):
    if not(len(new_time_indices_list_emulator)==0) and new_time_indices_list_emulator[-1]==time_idx:
        new_cycle_number_list[-1].append(cycle_number_list[idx])
        print("ALERT: ",new_cycle_number_list[-1])

    else:
        new_time_indices_list_emulator.append(time_idx)
        new_cycle_number_list.append([cycle_number_list[idx]])

time_indices_start = new_time_indices_list_emulator[0]

print("###Emulator data###")
for idx, time in enumerate(new_time_indices_list_emulator):
    print(f"time: {time}, cycle: {new_cycle_number_list[idx]}")


### ping_log parsing        
with open(input_path+files_list[1],'r') as file:
    file_content = file.read()
    
lines_list = file_content.split('\n')

splitted_lines_list = []
for line in lines_list:
    words_list = delete_elements(line.split(' '),'')
    splitted_lines_list.append(words_list)
    
time_indices_list_ping = []
RTT_list = []

ping_flag = False
for idx, line in enumerate(splitted_lines_list):
    if len(line)>3:
        curr_time_index = line[2]
        
        if time_indices_start<curr_time_index:
            ping_flag = True

        if ping_flag:            
            curr_RTT = float(line[9][5:])
            if not(len(time_indices_list_ping)==0) and time_indices_list_ping[-1]==curr_time_index:
                RTT_list[-1].append(curr_RTT)

            else:
                # if len(time_indices_list_ping)>0:
                #     n = len(RTT_list[-1])
                #     RTT_list[-1] = sum(RTT_list[-1])/n
                time_indices_list_ping.append(curr_time_index)
                RTT_list.append([curr_RTT])
    else:
        break


print("###Ping data###")
for idx, time in enumerate(time_indices_list_ping):
    print(f"time: {time}, RTT_list: {RTT_list[idx]}")

print("iperf len: ",len(bit_rate_list))
print("ping len: ",len(RTT_list))
print("Emulator len: ",len(new_time_indices_list_emulator))

# intersection_time_indices = [x for x in time_indices_list_iperf if ((x in time_indices_list_ping) and (x in new_time_indices_list_emulator))]
# print("intersection time indices len: ",len(intersection_time_indices))
# time_indices_list_iperf = np.array(time_indices_list_iperf)
# time_indices_list_ping = np.array(time_indices_list_ping)
# new_time_indices_list_emulator = np.array(new_time_indices_list_emulator)

# logical_idx_arr_iperf = np.ones(time_indices_list_iperf.size)==0
# for time_idx in intersection_time_indices:
#     logical_idx_arr_iperf = np.logical_or(logical_idx_arr_iperf,time_indices_list_iperf==time_idx) 

# logical_idx_arr_ping = np.ones(time_indices_list_ping.size)==0
# for time_idx in intersection_time_indices:
#     logical_idx_arr_ping = np.logical_or(logical_idx_arr_ping,time_indices_list_ping==time_idx) 

# logical_idx_arr_emulator = np.ones(new_time_indices_list_emulator.size)==0
# for time_idx in intersection_time_indices:
#     logical_idx_arr_emulator = np.logical_or(logical_idx_arr_emulator,new_time_indices_list_emulator==time_idx) 

bit_rate_len = len(bit_rate_list)
cycle_num_len = len(new_cycle_number_list)
RTT_len = len(RTT_list)

min_len = min(bit_rate_len,cycle_num_len,RTT_len)

bit_rate_list = np.array(bit_rate_list)
retransmission_list = np.array(retransmission_list)
RTT_list = np.array([x[0] for x in RTT_list])
new_cycle_number_list = np.array([x[0] for x in new_cycle_number_list])

bit_rate_list = bit_rate_list[:min_len]
retransmission_list = retransmission_list[:min_len]
RTT_list = RTT_list[:min_len]
new_cycle_number_list = new_cycle_number_list[:min_len]
new_time_indices_list_emulator = np.array(new_time_indices_list_emulator)[:min_len]


# print("cycle number list:\n",new_cycle_number_list)

# print("logical idx arr ping:\n",logical_idx_arr_ping," ",sum(logical_idx_arr_ping))
# print("logical idx arr emulator:\n",logical_idx_arr_emulator," ",sum(logical_idx_arr_emulator))
# selected_bit_rate_list = bit_rate_list[logical_idx_arr_iperf]
# selected_retransmission_list = retransmission_list[logical_idx_arr_iperf]
# selected_RTT_list = RTT_list[logical_idx_arr_ping]
# selected_cycle_number_list = new_cycle_number_list[logical_idx_arr_emulator]

# for idx, time in enumerate(intersection_time_indices):
#     print(f"time: {time}, bit_rate: {selected_bit_rate_list[idx]}, retransmission: {selected_retransmission_list[idx]}, RTT: {selected_RTT_list[idx]}, cycle: {cycle_number_list[idx]}")

os.makedirs(output_plots_path,exist_ok=True)

plt.plot(np.arange(min_len),bit_rate_list)
plt.xlabel('time')
plt.ylabel('Throughput')
plt.title('variation of Throughput across time')
plt.grid(True)
plt.ylim(0,140)
plt.savefig(output_plots_path+'Throughput_plot.jpg')
plt.show()


plt.plot(np.arange(min_len),retransmission_list)
plt.xlabel('time')
plt.ylabel('Retransmission')
plt.title('variation of retransmission across time')
plt.grid(True)
plt.ylim(0,2000)
plt.savefig(output_plots_path+'retransmissions_plot.jpg')
plt.show()

plt.plot(np.arange(min_len),RTT_list)
plt.xlabel('time')
plt.ylabel('RTT')
plt.title('variation of RTT across time')
plt.grid(True)
plt.ylim(0,500)
plt.savefig(output_plots_path+'RTT_plot.jpg')
plt.show()

print("input case: ",input_path)
print("Throughput mean: ",np.mean(bit_rate_list))
print("Throughput std_dev: ",np.std(bit_rate_list))
print("RTT mean: ",np.mean(RTT_list))
print("RTT std_dev: ",np.std(RTT_list))
print("Retransmission mean: ",np.mean(retransmission_list))
print("Retransmission std_dev: ",np.std(retransmission_list))