"""
Description:

"""

from subprocess import Popen, PIPE
import time
import numpy as np
cmd_list = ["C:\\Radiance\\bin\\gendaymtx",
            "-O0",
            "-m", "1",
            r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Desktop\BinaryRead\DNK_Copenhagen.061800_IWEC.wea"]

start = time.time()
p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate(b"This is stdin (type:bytes)")
rc = p.returncode
end = time.time()
dureation = end - start


start = time.time()
a = output.decode()
end = time.time()
dureation2 = end - start



start = time.time()
sky_matrix = np.zeros((146,8760), dtype = np.float64)
all_data = a.split("\r\n\r\n")
del all_data[0]
del all_data[-1]
for i, year in enumerate(all_data):
    year_split = year.split("\r\n")
    for j, hour in enumerate(year_split):
        sky_matrix[i][j] = hour.split(" ")[0]

end = time.time()
dureation3 = end - start

"""
start = time.time()
b = a.split("\n")
sky_matrix = np.zeros((146,8760), dtype = np.float64)
k = 8
for i in range(146):
    for j in range(8760):
        sky_matrix[i][j] = float(b[k].split(" ")[0])
        k += 1
end = time.time()
dureation3 = end - start
"""


#%%

"""
#Reading header
for i in range(20): #Maximum 20 lines for header
    if "NROWS" in b[i]:
        nrows = int(b[i].split("=")[-1])
    elif "NCOLS" in b[i]:
        ncols = int(b[i].split("=")[-1])
    elif "NCOMP" in b[i]:
        ncomp = int(b[i].split("=")[-1])
    elif "FORMAT" in b[i]:
        startline = i + 2
        break
"""


#%%
def run_command(info,
                cmd_list, 
				output_file_path = False,
                input_file_path = False):
    
    
	#Setting enviromental variable PATH
    os.environ["PATH"] = f"{info.radiance_bin};{info.accelerad_bin};" \
		+ "{}".format(os.environ["PATH"])
	
	#Setting enviromental variable RAYPATH
    os.environ["RAYPATH"] = f".;{info.radiance_lib};{info.accelerad_lib};"

    print("START - Subprocess: {}".format(cmd_list[0]))
	
	# Run process
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    if input_file_path != False:
        
        output, err = p.communicate(read_stdin(input_file_path))
    else:
        output, err = p.communicate(b"This is stdin (type:bytes)")
    rc = p.returncode
    
    if rc != 0:
        print(f"Error code: \n {err}")
	
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
	

	#Saving output in plain text
    if output_file_path:
        print("START - Writing ASCII data")
        with open(output_file_path, "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")