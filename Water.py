#imports
import pandas as pd

#list file names to read from
filename1 = "./Hays_County_wells_TableToExcel.xlsx"
filename2 = "./Results.xlsx"
filename3 = "./SDRainfall.xlsx"

#make objects from the excel sheets
wDepths = pd.read_excel(filename1)
rWater = pd.read_excel(filename2)
sdWater = pd.read_excel(filename3)


#make lists from the excel sheets
wDepthsList = wDepths["Hays_County_Wells.SeaLevelDepth"].tolist()
rWaterDepths = rWater["Hip(t) = input depth (m)"].tolist()
pTotal = rWater["Population"].tolist()
sdWaterDepths1 = sdWater["Hip(t) (-2)"].tolist()
sdWaterDepths2 = sdWater["Hip(t) (+2)"].tolist()

#list variables needed
base = 164
porosity = 0.45
area = 1756605010
i = 0
j = 0
wellOutput = []
wellOutput1 = []
wellOutput2 = []
wellDepth = []
wellDepth1 = []
wellDepth2 = []
totalDepth = [base]
totalDepth1 = [base]
totalDepth2 = [base]
dWells = []

#nested for loop to go through all years and wells each year
for i in range(0,53):
    temp = float(0)
    temp2 = 0
    temp3 = 0
    temp4 = 0
    #goes through the wells
    for j in range(0,166):
        #adds 146 cubic meters the total each year if the well is below the water table
        if wDepthsList[j] < totalDepth[i]:
            temp += 80000 #approximate amount of m^3 of water pumped per well per year
        else:
            #testing variable to see how many wells fell under the water table
            temp2 += 1
        if wDepthsList[j] < totalDepth1[i]:
            temp3 += 80000
        if wDepthsList[j] < totalDepth2[i]:
            temp4 += 80000
    #computs and adds the values into a list
    dWells.append(temp2)
    temp = temp + float(pTotal[i])*200 #annual water usage pere well per person in meters cubed
    temp3 = temp3 + float(pTotal[i])*200
    temp4 = temp4 + float(pTotal[i])*200
    wellOutput.append(temp)
    wellOutput1.append(temp3)
    wellOutput2.append(temp4)
    wellDepth.append((temp/area)/porosity)
    wellDepth1.append((temp3/area)/porosity)
    wellDepth2.append((temp4/area)/porosity)
    totalDepth.append(totalDepth[i] + (rWaterDepths[i] - wellDepth[i]))
    totalDepth1.append(totalDepth1[i] + (sdWaterDepths1[i] - wellDepth1[i]))
    totalDepth2.append(totalDepth2[i] + (sdWaterDepths2[i] - wellDepth2[i]))

### Testing Outputs
#/////////////////////////////
#print("well depths\n", wDepthsList)
#print("")           
#print("Population\n", pTotal[0:51])
#print("")
#print ("well output\n", wellOutput)
#print("")
#print("well depth\n", wellDepth)
#print("")
#print("total depth\n", totalDepth)
#print("")
#print("Dried wells\n", dWells)
#print(dWells)
#/////////////////////////////

#prints out the outputs into excel 
df = pd.DataFrame(list(zip(wellOutput,wellDepth,totalDepth)), columns=["QW", "Hop", "Zw"])
df.to_excel("Outputs_Test.xlsx")
df2 = pd.DataFrame(list(zip(wellOutput1,wellOutput2,wellDepth1,wellDepth2,totalDepth1,totalDepth2)), columns=["Qw (-2)","Qw (+2)","Hop (-2)","Hop (+2)", "Zw (-2)","Zw (+2)"])
df2.to_excel("SDOutputs.xlsx")