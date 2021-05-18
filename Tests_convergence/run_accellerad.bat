for ab in 6 8 10 12 ; do
for ad in 1024 4096 16384 65536 262142 ; do
for lw_power in 1 1.5 2 2.5 3 ; do
lw = 1 / (ad^lw_power)

rcontrib ... -ab $ab -ad $ad -lw $lw ...  < fewpoints.txt > result_${ab}_${ad}_${lw}.mtx

done; done; done