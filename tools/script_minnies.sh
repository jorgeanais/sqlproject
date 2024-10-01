#!/bin/bash

files=(
    "/home/jorge/Documents/data/hst/Minni144/ifb444k0q_flc.fits"
    "/home/jorge/Documents/data/hst/Minni144/ifb444kdq_flc.fits"
    "/home/jorge/Documents/data/hst/Minni144/ifb444kbq_flc.fits"
    "/home/jorge/Documents/data/hst/Minni144/ifb444juq_flc.fits"
    "/home/jorge/Documents/data/hst/Minni144/ifb444jvq_flc.fits"
    "/home/jorge/Documents/data/hst/Minni144/ifb444kiq_flc.fits"
    "/home/jorge/Documents/data/hst/Minni146/ifb446bzq_flc.fits"
    "/home/jorge/Documents/data/hst/Minni146/ifb446brq_flc.fits"
    "/home/jorge/Documents/data/hst/Minni146/ifb446btq_flc.fits"
    "/home/jorge/Documents/data/hst/Minni146/ifb446bvq_flc.fits"
    "/home/jorge/Documents/data/hst/Minni146/ifb446bqq_flc.fits"
    "/home/jorge/Documents/data/hst/Minni146/ifb446bxq_flc.fits"
    "/home/jorge/Documents/data/hst/Minni330/ifb430f4q_flc.fits"
    "/home/jorge/Documents/data/hst/Minni330/ifb430f8q_flc.fits"
    "/home/jorge/Documents/data/hst/Minni330/ifb430f2q_flc.fits"
    "/home/jorge/Documents/data/hst/Minni330/ifb430f1q_flc.fits"
    "/home/jorge/Documents/data/hst/Minni330/ifb430faq_flc.fits"
    "/home/jorge/Documents/data/hst/Minni330/ifb430f6q_flc.fits"
)


for file in "${files[@]}"
do
    echo "Processing: $file"
    python main.py -f "$file" --hmin 3 --fmin 10 --name "Run01_hmin3fmin10" --description "20241001_attempt01"
    echo "-----------------------------"
done


