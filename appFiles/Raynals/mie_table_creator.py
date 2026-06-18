from   dlsAnalyzer       import *
from simulation_helpers import mieIntensity

wavelengths = [405,633,658,660,817]
angles      = [15,90,147,150,173]

# Initialize an empty 3D numpy array to store the intensity values
intensity_3d = np.empty((len(wavelengths), len(angles), 200))  # Assuming 200 hr values

for i, lambda0 in enumerate(wavelengths):
    for j, angle in enumerate(angles):


        dls               = dlsAnalyzer()
        l                 = dls.loadExperiment("./www/test.csv","test")
        d                 = dls.experimentsOri["test"] 

        d.lambda0         = lambda0                #  Laser wavelength in nanometers
        d.scatteringAngle = angle / 180 * np.pi  #  Angle of detection in radians
        d.getQ()                               #  Calculate the Bragg wave vector
        d.createFittingS_space(0.09,1e6,200)   #  Discretize the decay rate space we will use for the fitting

        intensity = mieIntensity(
            hr=d.hrs,
            angle=angle, # Already in degrees
            lambda0=lambda0,
            refractiveIndex=d.refractiveIndex).flatten()
        
        intensity_3d[i, j, :] = intensity

        print(len(intensity))

    print(i)

# Export the 3D array to a .npy file
np.save('mie_intensity_lookup_table.npy', intensity_3d)

# Save the wavelengths and angles used in separate .npy files
np.save('wavelengths.npy', np.array(wavelengths))
np.save('angles.npy', np.array(angles))

# Save the HR values used in a separate .npy file (assuming they are the same for all combinations of wavelength and angle)
np.save('hr_values.npy', d.hrs)


# Export a README file with the wavelengths and angles used
with open('README_mie_lookup_table.txt', 'w') as f:
    f.write("Wavelengths (nm) as first dimension: " + ", ".join(map(str, wavelengths)) + "\n")
    f.write("Angles (degrees) as second dimension: " + ", ".join(map(str, angles)) + "\n")
    f.write("Third dimension corresponds to the intensity values for 200 hr values.")
