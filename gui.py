import h5py
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename
from curveFitting import exponentialFit, fourierFit, gaussian


class HDF5PlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HDF5 Data Plotter")

        # Initialize variables
        self.filepath = None
        self.group_names = []
        self.dataset_names = []
        self.dataset_map = {}
        self.selected_group = tk.StringVar()
        self.selected_dataset1 = tk.StringVar()
        self.selected_dataset2 = tk.StringVar()

        # Build the GUI
        self.build_gui()

    def build_gui(self):
        # File selection button
        file_frame = ttk.Frame(self.root)
        file_frame.pack(pady=10)

        open_button = ttk.Button(file_frame, text="Open HDF5 File", command=self.open_file)
        open_button.pack()

        # Group selection frame
        group_frame = ttk.LabelFrame(self.root, text="Select Group")
        group_frame.pack(padx=10, pady=10, fill="x")

        # Dropdown for group selection
        ttk.Label(group_frame, text="Group:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.group_combo = ttk.Combobox(group_frame, textvariable=self.selected_group, state="readonly")
        self.group_combo.grid(row=0, column=1, padx=5, pady=5, sticky="we")
        self.group_combo.bind("<<ComboboxSelected>>", self.group_selected)

        # Dataset selection frame
        dataset_frame = ttk.LabelFrame(self.root, text="Select Datasets")
        dataset_frame.pack(padx=10, pady=10, fill="x")

        # Dropdown for first dataset
        ttk.Label(dataset_frame, text="Dataset 1:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.dataset_combo1 = ttk.Combobox(dataset_frame, textvariable=self.selected_dataset1, state="readonly")
        self.dataset_combo1.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        # Dropdown for second dataset
        ttk.Label(dataset_frame, text="Dataset 2:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.dataset_combo2 = ttk.Combobox(dataset_frame, textvariable=self.selected_dataset2, state="readonly")
        self.dataset_combo2.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Plot button
        plot_button = ttk.Button(self.root, text="Plot Datasets", command=self.plot_datasets)
        plot_button.pack(pady=10)

        # Configure grid weights
        group_frame.columnconfigure(1, weight=1)
        dataset_frame.columnconfigure(1, weight=1)

    def open_file(self):
        # Open file dialog
        filepath = askopenfilename(filetypes=[("HDF5 files", "*.h5"), ("All files", "*.*")])
        if filepath:
            self.filepath = filepath
            self.load_groups()

    def load_groups(self):
        # Load the HDF5 file and extract group names
        try:
            self.hdf5_file = h5py.File(self.filepath, 'r')
            self.group_names = list(self.hdf5_file.keys())
            # Update the group combobox
            self.group_combo['values'] = self.group_names
            self.selected_group.set('')
            self.dataset_names = []
            self.dataset_map = {}
            self.dataset_combo1['values'] = []
            self.dataset_combo2['values'] = []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load HDF5 file:\n{e}")
    
    def group_selected(self, event):
        selected_group = self.selected_group.get()
        if selected_group:
            # Collect datasets within the selected group
            self.dataset_names = []
            self.dataset_map = {}
            group = self.hdf5_file[selected_group]
            group.visititems(self.collect_datasets)
            # Update dataset comboboxes
            self.dataset_combo1['values'] = self.dataset_names
            self.dataset_combo2['values'] = self.dataset_names
            self.selected_dataset1.set('')
            self.selected_dataset2.set('')

    def collect_datasets(self, name, obj):
        # Collect names of datasets within the selected group
        if isinstance(obj, h5py.Dataset):
            # The full path is self.selected_group + '/' + name
            full_path = f"{self.selected_group.get()}/{name}"
            # Adjust the name to omit redundant parts
            # For example, remove 'dev2467/demods/4/sample/' prefix
            prefix_to_remove = 'dev2467/demods/4/sample/'
            if name.startswith(prefix_to_remove):
                adjusted_name = name[len(prefix_to_remove):]
            else:
                adjusted_name = name
            self.dataset_names.append(adjusted_name)
            self.dataset_map[adjusted_name] = full_path

    def plot_datasets(self):
        # Get selected datasets
        dataset1_name = self.selected_dataset1.get()
        dataset2_name = self.selected_dataset2.get()
        if not dataset1_name or not dataset2_name:
            messagebox.showwarning("Selection Error", "Please select two datasets to plot.")
            return
        try:
            # Get full dataset paths
            dataset1_full_path = self.dataset_map[dataset1_name]
            dataset2_full_path = self.dataset_map[dataset2_name]
            # Extract datasets
            data1 = self.hdf5_file[dataset1_full_path][:]
            data2 = self.hdf5_file[dataset2_full_path][:]
            # Perform Gaussian fit on data2 vs data1
            initial_guess = [np.max(data2), data1[np.argmax(data2)], 1.0, np.min(data2)]
            popt, _ = curve_fit(gaussian, data1, data2, p0=initial_guess)
            gaussian_fit = gaussian(data1, *popt)
            # Plot datasets and the fit
            plt.figure(figsize=(10, 6))
            plt.plot(data1, data2, label='Data')
            plt.plot(data1, gaussian_fit, '-', label='Gaussian Fit')
            plt.xlabel(dataset1_name)
            plt.ylabel(dataset2_name)
            plt.title(f"{dataset1_name} vs {dataset2_name}")
            plt.legend()
            plt.grid(True)
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to plot datasets:\n{e}")



if __name__ == "__main__":
    root = tk.Tk()
    app = HDF5PlotterApp(root)
    root.mainloop()