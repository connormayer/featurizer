import Featurizer
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

window_height = 300
window_width = 400


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Featurizer")
        self.minsize(window_width, window_height)
        #self.wm_iconbitmap(())
        #self.configure(background='#4D4D4D')

        # center the window
        positionRight = int((self.winfo_screenwidth() / 2) - (window_width / 2))
        positionDown = int((self.winfo_screenheight() / 2) - (window_height / 2))

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))

        self.labelFrame = ttk.LabelFrame(self, text="Select a file")
        self.labelFrame.grid(column=5, columnspan=3, row=4, padx=100, pady=20)
        self.labelFrame2 = ttk.LabelFrame(self, text="Select type")
        self.labelFrame2.grid(column=5, row=14, padx=1, pady=20)
        self.labelFrame3 = ttk.LabelFrame(self, text="Featurization type")
        self.labelFrame3.grid(column=6, row=14, padx=1, pady=20)
        self.labelFrame4 = ttk.LabelFrame(self, text="Options")
        self.labelFrame4.grid(column=7, row=14, padx=1, pady=20)
        self.labelFrame5 = ttk.LabelFrame(self, text="Save a file")
        self.labelFrame5.grid(column=5, columnspan=3, row=24, padx=100, pady=20)

        #################################################
        ##                INPUT BUTTON                 ##
        #################################################

        lbl = Label(self.labelFrame, text="Input file")
        lbl.grid(column=0, row=0, padx=20)
        self.filename_input = ""
        self.button_browse_input()

        #################################################
        ##          RADIO BUTTON - SELECT TYPE         ##
        #################################################
        self.v = IntVar(None, 2)

        Radiobutton(self.labelFrame2,
                    indicatoron=0,
                    text="featurization",
                    variable=self.v,
                    value=2).pack(anchor=W, fill=X)
        Radiobutton(self.labelFrame2,
                    indicatoron=0,
                    text="Poset",
                    variable=self.v,
                    value=1).pack(anchor=W, fill=X)

        #################################################
        ##       RADIO BUTTON - FEATURIZATION TYPE     ##
        #################################################
        MODES = [
            ('complementary', 1),
            ('privative', 2),
            ('inferential_complementary', 3),
            ('full', 4)
        ]
        self.featurization = StringVar(None, 'complementary')

        for text, value in MODES:
            Radiobutton(self.labelFrame3,
                        indicatoron=0,
                        text=text,
                        variable=self.featurization,
                        value=text).pack(anchor=W, fill=X)

        self.specification = Featurizer.FEATURIZATION_MAP.get(self.featurization.get(), self.featurization.get())

        #################################################
        ##               CHECK BOX - OPTIONS           ##
        #################################################

        self.use_numpy = BooleanVar()
        Checkbutton(self.labelFrame4,
                    text="numpy",
                    variable=self.use_numpy).pack(anchor=W, fill=X)

        self.verbose = BooleanVar()
        Checkbutton(self.labelFrame4,
                    text="verbose",
                    variable=self.verbose).pack(anchor=W, fill=X)

        #################################################
        ##               OUTPUT BUTTONS                ##
        #################################################

        lbl2 = Label(self.labelFrame5, text="Output file")
        lbl2.grid(column=0, row=0, padx=20, pady=10)

        self.button_browse_output_CSV()
        self.button_browse_output_GV()
        self.button_browse_output_PNG()

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
        button = ttk.Button(self.labelFrame, text="Browse", command=self.fileDialog)
        button.grid(column=1, row=0)

    def fileDialog(self):
        '''
            command associated with Browse Button for filename_input
            Allowed filetype: .txt
        '''
        self.filename_input = filedialog.askopenfilename(initialdir="./", title="Select a file",
                                                         filetype=(("TXT", "*.txt"), ("All Files", "*.*")))
        label_input = ttk.Label(self.labelFrame, text="")
        label_input.grid(column=2, row=0)
        label_input.configure(text=self.filename_input)

    def button_browse_output_PNG(self):
        ''' Browse button to output PNG file based on the selected options '''
        button = ttk.Button(self.labelFrame5, text="PNG", command=self.fileDialogSave_PNG)
        button.grid(column=1, row=0)

    def fileDialogSave_PNG(self):
        '''
            command associated with Browse Button for output_PNG
            Allowed filetype: .png
        '''
        if self.input_validation():
            return

        filename_default = self.generate_default_filename()
        filename_output = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            filetypes=[("PNG", "*.png")],
            defaultextension='.png',
            initialdir="./",
            initialfile=filename_default,
            title="Choose a file name"
        )
        if not filename_output:
            return

        featurizer, *_ = self.init_featurizer()
        filename_temp = filename_output.rsplit('/', 1)[0] + '/temp.temp'
        if self.v.get() == 1:
            featurizer.graph_poset(filename_temp)
        elif self.v.get() == 2:
            featurizer.graph_feats(filename_temp)

        featurizer.dot_to_png(filename_temp, filename_output)

    def button_browse_output_GV(self):
        ''' Browse button to output GV file based on the selected options '''
        button = ttk.Button(self.labelFrame5, text="GV", command=self.fileDialogSave_GV)
        button.grid(column=3, row=0)

    def fileDialogSave_GV(self):
        '''
            command associated with Browse Button for output_GV
            Allowed filetype: .gv
        '''
        if self.input_validation():
            return

        filename_default = self.generate_default_filename()
        filename_output = filedialog.asksaveasfilename(
            confirmoverwrite=True,
            filetypes=[("GV", "*.gv")],
            defaultextension='.gv',
            initialdir="./",
            initialfile=filename_default,
            title="Choose a file name"
        )
        if not filename_output:
            return

        featurizer, *_ = self.init_featurizer()
        if self.v.get() == 1:
            featurizer.graph_poset(filename_output)
        elif self.v.get() == 2:
            featurizer.graph_feats(filename_output)

    def button_browse_output_CSV(self):
        ''' Browse button to output CSV file based on the selected options '''
        button = ttk.Button(self.labelFrame5, text="CSV", command=self.fileDialogSave_CSV)
        button.grid(column=2, row=0)

    def fileDialogSave_CSV(self):
        '''
            command associated with Browse Button for output_CSV
            Allowed filetype: .csv
        '''
        if self.input_validation():
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
        button.grid(column=4, row=0, padx=20)

    def print_new_window(self):
        '''
            command associated with print button
            Pops up new window
        '''
        if self.input_validation():
            return
        featurizer, verbose_text = self.init_featurizer()

        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(root)

        # sets the title of the
        # Toplevel widget
        newWindow.title("Print")

        text_print = verbose_text + featurizer.print_featurization_helper() + \
                     featurizer.print_segment_features_helper()

            # A Label widget to show in toplevel
        text1 = Text(newWindow, height=60, width=150)
        text1.insert(END, text_print)
        text1.config()
        text1.pack()

    def input_validation(self):
        ''' Checks if input filename has been selected '''
        if self.filename_input is "":
            messagebox.showinfo("Error", "Please select an input file")
            return True
        self.specification = Featurizer.FEATURIZATION_MAP.get(self.featurization.get(), self.featurization.get())
        return False

    def generate_default_filename(self):
        inv_map = {v: k for k, v in Featurizer.FEATURIZATION_MAP.items()}
        filename_default = "{}_{}".format(
            self.filename_input.rsplit('/', 1)[1].rsplit('.', 1)[0], inv_map[self.specification]
        )
        return filename_default


if __name__ == '__main__':
    root = Root()
    root.mainloop()
