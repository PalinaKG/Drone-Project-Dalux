### Before running the code
* There are two inputs that are needed for the code, the first one being a list of coordinates that covers the area needed. The coordinates need to be saved in a file called "data.json" in the following format:

[
{"x":55.65239629285622,"y":12.5759143686295},
{"x":55.65121890082774,"y":12.57590900421147},
{"x":55.6512279811074,"y":12.574181661605879},
{"x":55.65239931952541,"y":12.574192390441938}
]

* The second input needed to provide is the flight height, that can be changed in the main.py file using the variable flight_height. 
* The input needs to be a float number
* The default flight height is 2m
* The drone does not have any obstacle detection, any obstacles therefore need to be excluded from the area or the flight height made high enough to fly over any obstacle
* The code needs to be run using Ubuntu
* install all the libraries in the requirements.txt using the following command:
 * pip install -r requirements.txt
 
### Flying the drone
* Turn on the drone
* Connect to the Wifi: ANAFI-A126355
* Place the drone on the ground close to the area you want to capture
* Make sure there are no obstacles between the initial location and the start of the area
* Stand few meters away from the drone, but not in between the drone and the area of interest

Run the following commands in the terminal:
* source ~/code/parrot-groundsdk/products/olympe/linux/env/shell
* source ~/venv/bin/activate
* python main.py
 
Troubleshooting if the code does not work
* Start by restarting the drone:
 * Make sure that the drone is turned on
 * Hold down the power button until all the lights have turned red, then release the button, the drone will turn on and off automatically
* The drone might also need to be calibrated, for that the SkyController and a phone needs to be used:
 * First the FreeFlight6 app needs to be downloaded on your phone
 * Then your phone needs to be connected to the SkyController through a cord
 * Open the FreeFlight6 app
 * Press the Fly button
 * Then a instructions to calibrate the drone should appear on the screen if the drone needs to be calibrated
 * Follow the instructions on the screen
 
 
### Fetching the images
You can either fetch the images by a certain date, by the most recent date or all the images on the drone. You can also choose whether the selected images should be deleted or not. Run the following script:
* python download_pics.py
* Follow the instructions on the screen to choose which images should be fetched and if they should be deleted or not

### Stitching the images together
First make sure you have the correct folder structure, run the following commands, remember to replace "NAME OF FOLDER" with the name of the folder containing the images you want to stitch and YOUR PATH with your path to the datasets folder:
Make sure to have docker downloaded
* mkdir datasets && cd datasets && mkdir project && cd project && mkdir images && cd images && cd ../../..
Copy the images to the images folder you just created:
* cp -a /"NAME OF FOLDER"/. ./datasets/project/images
Run the following command to stitch the photos together:
* docker run -ti --rm -v "YOUR PATH"/datasets:/datasets opendronemap/odm --project-path /datasets project --orthophoto-resolution 0.5 --min-num-features 9000 SKOÐA HVAÐA TÖLUR VIÐ SKILUM!!!
* The stitched image 
Before running the image stitching command again the docker image needs to be deleted and all the folders in project need to be removed
* rm -r datasets
* docker rmi opendronemap/odm 