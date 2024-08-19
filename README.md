# sqlproject

A Python wrapper for the HST1PASS routine.

0. Modify the settings file accordingly.
1. To initialize the DB, run `python -m project.initialize`. It also works if you need to update the paths to the images or PSF.
2. To execute the hst1pass routine run: `python main.py -f something_xxx.fits --hmin 5 --fmin 2500`. Notice that the image has to be registered in the database. At the moment, the corresponding PSF file should already be registered in the database.
