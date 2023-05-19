import numpy as np
import visualization  # noqa
from abaqus import *
from abaqusConstants import *
from driverUtils import *

executeOnCaeStartup()

# Open output database
odb = session.openOdb("element.odb")

# Show the output database in viewport
session.viewports["Viewport: 1"].setValues(displayedObject=odb)

# Extract output data
dataList = session.xyDataListFromField(
    odb=odb, outputPosition=NODAL, variable=(("U", NODAL, ((COMPONENT, "U3"),)),), nodeSets=("INSTANCE.SET-TOP",)
)

data = np.array(dataList[0])
np.savetxt("U3.csv", data, header="time,U3", delimiter=",", comments="")
