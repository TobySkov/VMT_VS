"""
Description:

"""

no_triangles_list = []
no_points_list = []
for i in range(5):
    for j in range(10):
        no_triangles_list.append(3500*4**i)
        no_points_list.append(4**(j+1))
        
with open("To_gitignore.txt", "w") as outfile:
    for i in range(50):
        outfile.write(f"Tests_raytracing/Triangles_{no_triangles_list[i]}__Points_{no_points_list[i]}\n")