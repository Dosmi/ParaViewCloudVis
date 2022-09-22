# NOTE: THIS SCRIPT REQUIRES h5py MODULE TO BE INSTALLED ON THE SYSTEM


# Code for 'Script'
print("Running ... ")
from vtk.numpy_interface import algorithms as algs
from vtk.numpy_interface import dataset_adapter as dsa
import numpy as np

import glob, os


import h5py
BASE_PATH = '/work/e710/shared/pmpic598/'
FILE_NAME = BASE_PATH + 'parcels_00000_00598.nc'

os.chdir(BASE_PATH)

ncfiles = []

for file in glob.glob("*.nc"):
    #print(file)
    ncfiles.append(file)

data = dict()
dataarray = dict()
allkeys = []

with h5py.File(FILE_NAME, mode='r') as f:
	# List available datasets.
	print (f.keys())
	
	for key in f.keys():
        dataarray[key] = f.get(key)[()]
        allkeys.append(key)


print("Imports finished")


for FILE_IT in ncfiles[1:]:
    print(FILE_IT)
    with h5py.File(FILE_IT, mode='r') as f:
	    # List available datasets.
	    #print (f.keys())
	
	    for key in f.keys():
		    dataarray[key] = np.append(dataarray[key], f.get(key)[()])


for keyprop in allkeys:
    print(keyprop)
    data[keyprop] = numpy.array(dataarray[keyprop])

# convert the 3 arrays into a single 3 component array for
# use as the coordinates for the points.
coordinates = algs.make_vector(data["x"], data["y"], data["z"])

# create a vtkPoints container to store all the
# point coordinates.
pts = vtk.vtkPoints()

# numpyTovtkDataArray is needed to called directly to convert the NumPy
# to a vtkDataArray which vtkPoints::SetData() expects.
pts.SetData(dsa.numpyTovtkDataArray(coordinates, "b"))

# set the pts on the output.
output.SetPoints(pts)

# next, we define the cells i.e. the connectivity for this mesh.
# here, we are creating merely a point could, so we'll add
# that as a single poly vextex cell.
numPts = pts.GetNumberOfPoints()
# ptIds is the list of point ids in this cell
# (which is all the points)
ptIds = vtk.vtkIdList()
ptIds.SetNumberOfIds(numPts)
for a in range(numPts):
    ptIds.SetId(a, a)

# Allocate space for 1 cell.
output.Allocate(1)
output.InsertNextCell(vtk.VTK_POLY_VERTEX, ptIds)

print("Finished")

# We can also pass all the array read from the CSV
# as point data arrays.
for name in data.keys():
    array = data[name]
    output.PointData.append(array, name)

print("Done")
