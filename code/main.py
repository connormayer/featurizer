import Featurizer
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

window_height = 300
window_width = 400
FEAT = (0, 'featurization')
POSET = (1, 'poset')


class Root(tk.Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Featurizer")
        self.minsize(window_width, window_height)

        # center the window
        position_right = int((self.winfo_screenwidth() / 2) - (window_width / 2))
        position_down = int((self.winfo_screenheight() / 2) - (window_height / 2))

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(position_right, position_down))

        self.labelFrame = ttk.LabelFrame(self, text="Select a file")
        self.labelFrame.grid(column=5, columnspan=3, row=4, padx=100, pady=20)
        self.labelFrame3 = ttk.LabelFrame(self, text="Featurization type")
        self.labelFrame3.grid(column=5, row=14, padx=100, pady=20)
        self.labelFrame4 = ttk.LabelFrame(self, text="Options")
        self.labelFrame4.grid(column=6, row=14, padx=1, pady=20)
        self.labelFrame5 = ttk.LabelFrame(self, text="Save a file")
        self.labelFrame5.grid(column=5, columnspan=3, row=24, padx=100, pady=20)

        #################################################
        ##                INPUT BUTTON                 ##
        #################################################

        lbl = tk.Label(self.labelFrame, text="Input file")
        lbl.grid(column=0, row=0, padx=20)
        self.filename_input = ""
        self.button_browse_input()

        #################################################
        ##       RADIO BUTTON - FEATURIZATION TYPE     ##
        #################################################
        MODES = [
            ('privative', 1),
            ('complementary', 2),
            ('inferential_complementary', 3),
            ('full', 4)
        ]
        self.featurization = tk.StringVar(None, 'complementary')

        for text, value in MODES:
            tk.Radiobutton(self.labelFrame3,
                        indicatoron=0,
                        text=text,
                        variable=self.featurization,
                        value=text).pack(anchor=tk.W, fill=tk.X)

        self.specification = Featurizer.FEATURIZATION_MAP.get(self.featurization.get(), self.featurization.get())

        #################################################
        ##               CHECK BOX - OPTIONS           ##
        #################################################

        self.use_numpy = tk.BooleanVar()
        tk.Checkbutton(self.labelFrame4,
                    text="numpy",
                    variable=self.use_numpy).pack(anchor=tk.W, fill=tk.X)

        self.verbose = tk.BooleanVar()
        tk.Checkbutton(self.labelFrame4,
                    text="verbose",
                    variable=self.verbose).pack(anchor=tk.W, fill=tk.X)

        #################################################
        ##               OUTPUT BUTTONS                ##
        #################################################

        lbl2 = tk.Label(self.labelFrame5, text="Output file")
        lbl2.grid(column=0, row=0, padx=20, pady=10)

        self.button_browse_output_GV_feat()
        self.button_browse_output_PNG_feat()
        self.button_browse_output_GV_poset()
        self.button_browse_output_PNG_poset()
        self.button_browse_output_CSV()

        self.button_print()

    def init_featurizer(self):
        '''
            Initialize Featurizer object based on the user selected data

            Note:
                Selection required for: filename_input, filename_output, featurization type
        '''
        featurizer = Featurizer.Featurizer.from_file(
            self.filename_input, self.specification, use_numpy=self.use_numpy.get(),
            verbose=self.verbose.get()
        )
        verbose_text = featurizer.get_features_from_classes_helper()
        return featurizer, verbose_text

    def button_browse_input(self):
        ''' Browse Button for filename_input '''
        button = ttk.Button(self.labelFrame, text="Browse", command=self.file_dialog)
        button.grid(column=1, row=0)

    def file_dialog(self):
        '''
            command associated with Browse Button for filename_input
            Allowed filetype: .txt
        '''
        self.filename_input = filedialog.askopenfilename(initialdir="./", title="Select a file",
                                                         filetype=(("TXT", "*.txt"), ("All Files", "*.*")))
        label_input = ttk.Label(self.labelFrame, text="")
        label_input.grid(column=2, row=0)
        label_input.configure(text=self.filename_input)

    def button_browse_output_PNG_feat(self):
        ''' Browse button to output PNG (feat) file based on the selected options '''
        button = ttk.Button(self.labelFrame5,
                            text="Featurization graph as PNG",
                            command=lambda: self.file_dialog_save_PNG(FEAT))
        button.grid(column=1, row=0, sticky='ew')

    def button_browse_output_PNG_poset(self):
        ''' Browse button to output PNG (poset) file based on the selected options '''
        button = ttk.Button(self.labelFrame5,
                            text="Poset graph as PNG",
                            command=lambda: self.file_dialog_save_PNG(POSET))
        button.grid(column=1, row=1, sticky='ew')

    def file_dialog_save_PNG(self, output_type):
        '''
            command associated with Browse Button for output_PNG
            Allowed filetype: .png
        '''
        if not self.input_validation():
            return

        filename_default = self.generate_default_filename() + "_" + output_type[1]
        filename_output = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            filetypes=[("PNG", "*.png")],
            defaultextension='.png',
            initialdir="./",
            initialfile=filename_default,
            title="Choose a file name"
        )
        # file_dialog cancelled
        if not filename_output:
            return

        featurizer, *_ = self.init_featurizer()
        filename_temp = filename_output.rsplit('/', 1)[0] + '/temp.temp'
        if output_type == FEAT:
            featurizer.graph_feats(filename_temp)
        elif output_type == POSET:
            featurizer.graph_poset(filename_temp)

        try:
            featurizer.dot_to_png(filename_temp, filename_output)
        except Featurizer.ExecutableNotFound:
            messagebox.showerror("Missing graphviz",
                                 "Missing graphviz executable\n" +
                                 "Please visit https://graphviz.org to install graphviz")

    def button_browse_output_GV_feat(self):
        ''' Browse button to output GV (feat) file based on the selected options '''
        button = ttk.Button(self.labelFrame5,
                            text="Featurization graph as GV",
                            command=lambda: self.file_dialog_save_GV(FEAT))
        button.grid(column=2, row=0, sticky='ew')

    def button_browse_output_GV_poset(self):
        ''' Browse button to output GV (poset) file based on the selected options '''
        button = ttk.Button(self.labelFrame5,
                            text="Poset graph as GV",
                            command=lambda: self.file_dialog_save_GV(POSET))
        button.grid(column=2, row=1, sticky='ew')

    def file_dialog_save_GV(self, output_type):
        '''
            command associated with Browse Button for output_GV
            Allowed filetype: .gv
        '''
        if not self.input_validation():
            return

        filename_default = self.generate_default_filename() + "_" + output_type[1]
        filename_output = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            filetypes=[("GV", "*.gv")],
            defaultextension='.gv',
            initialdir="./",
            initialfile=filename_default,
            title="Choose a file name"
        )
        # file_dialog cancelled
        if not filename_output:
            return

        featurizer, *_ = self.init_featurizer()
        if output_type == FEAT:
            featurizer.graph_feats(filename_output)
        elif output_type == POSET:
            featurizer.graph_poset(filename_output)


    def button_browse_output_CSV(self):
        ''' Browse button to output CSV file based on the selected options '''
        button = ttk.Button(self.labelFrame5, text="CSV", command=self.file_dialog_save_CSV)
        button.grid(column=4, row=0, padx=20)

    def file_dialog_save_CSV(self):
        '''
            command associated with Browse Button for output_CSV
            Allowed filetype: .csv
        '''
        if not self.input_validation():
            return

        filename_default = self.generate_default_filename()
        filename_output = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            filetypes=[("CSV", "*.csv")],
            defaultextension='.csv',
            initialdir="./",
            initialfile=filename_default,
            title="Choose a file name"
        )
        if not filename_output:
            return

        featurizer, *_ = self.init_featurizer()
        featurizer.features_to_csv(filename_output)

    def button_print(self):
        ''' Button to print results based on the selected options '''
        button = ttk.Button(self.labelFrame5, text="print", command=self.print_new_window)
        button.grid(column=4, row=1, padx=20)

    def print_new_window(self):
        '''
            command associated with print button
            Pops up new window
        '''
        if not self.input_validation():
            return
        featurizer, verbose_text = self.init_featurizer()

        # Toplevel object which will
        # be treated as a new window
        new_window = tk.Toplevel(root)

        # sets the title of the
        # Toplevel widget
        new_window.title("Print")

        text_print = verbose_text + featurizer.print_featurization_helper() + \
                     featurizer.print_segment_features_helper()

        # A Label widget to show in toplevel
        text1 = tk.Text(new_window, height=60, width=150)
        text1.insert(tk.END, text_print)
        text1.config()
        text1.pack()

    def input_validation(self):
        ''' Checks if input filename has been selected '''
        if not self.filename_input:
            messagebox.showinfo("Error", "Please select an input file")
            return False
        self.specification = Featurizer.FEATURIZATION_MAP.get(self.featurization.get(), self.featurization.get())
        return True

    def generate_default_filename(self):
        inv_map = {v: k for k, v in Featurizer.FEATURIZATION_MAP.items()}
        filename_default = "{}_{}".format(
            self.filename_input.rsplit('/', 1)[1].rsplit('.', 1)[0], inv_map[self.specification]
        )
        return filename_default


if __name__ == '__main__':
    root = Root()
    root.mainloop()
