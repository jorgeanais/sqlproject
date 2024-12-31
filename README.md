# sqlproject

A Python wrapper for the HST1PASS routine.

0. Modify the settings file accordingly.
1. To initialize the DB, run `python -m project.initialize`. It also works if you need to update the paths to the images or PSF.
2. To execute the hst1pass routine run: `python main.py -f something_xxx.fits --hmin 5 --fmin 2500`. Notice that the image and the corresponding PSF file should already be registered in the database.

## Updates

2024-10-01 Fix problem of multiple targets and input file with complete path.
2024-10-01 Successfully processed flc images of MINNI144, MINNI146 and MINNI330
2024-12-31 Process all cluster flc images!  