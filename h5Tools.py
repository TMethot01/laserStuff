import h5py

with h5py.File("NoiseMeasurement_sweep_00000 (1).h5", "r") as f: # if you have a different file name change this.
    with open('fileStructure.txt', 'w') as outfile:

        def print_structure(name, obj):
            level = name.count('/')
            indent = '  ' * level
            outfile.write(f"{indent}{name.split('/')[-1]}\n")

        def write_name(name):
            outfile.write(name + '\n')
        
        #f.visit(write_name)  # Gives full group list
        f.visititems(print_structure)  # Gives indented file structure