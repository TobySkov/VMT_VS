"""
Oconv call
"""
import os
from subprocess import Popen, PIPE


#Setting enviromental variable PATH
os.environ["PATH"] = "C:\\Accelerad\\bin;" + \
    "C:\\Radiance\\bin;" + \
    "{}".format(os.environ["PATH"])
    
#Setting enviromental variable RAYPATH
os.environ["RAYPATH"] = ".;" + \
    "C:\\Accelerad\\lib;" + \
    "C:\\Radiance\\lib"




cmd_list = [r"C:\\Radiance\\bin\\oconv.exe",
            r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\Triangles_3500__Points_4096\Radiance\model\aperture\aperture.mat",
            r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\Triangles_3500__Points_4096\Radiance\model\aperture\aperture.rad",
            r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\Triangles_3500__Points_4096\Radiance\model\scene\envelope.mat",
            r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\Triangles_3500__Points_4096\Radiance\model\scene\envelope.rad",
            r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\Triangles_3500__Points_4096\Radiance\model\scene\shades.mat",
            r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\Triangles_3500__Points_4096\Radiance\model\scene\shades.rad"
            ]


output_filename = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT_VS\Tests_convergence\convergence_geo.oct"

#%%


print("START - Subprocess: {}".format(cmd_list[0]))
p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate(b"This is stdin")
rc = p.returncode
if rc != 0:
    print(f"Error code: \n {err}")
print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))

print("START - Writing ASCII data")
with open(output_filename, "wb") as outfile:
    outfile.write(output)
print("DONE  - Writing ASCII data")
    
