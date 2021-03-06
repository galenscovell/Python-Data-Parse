
import sys, os.path, time, xlrd, re

import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

from tkinter import *
from tkinter import ttk, font, messagebox




class MainWindow():
    """Parser GUI."""

    def __init__(self, root):
        self.root = root
        self.regular_font = font.Font(family='DejaVu Sans Mono', size=10)
        self.dataframe = ''
        self.state = ''
        self.column_choice = ''
        self.search_term = ''
        self.custom_chart_terms = []


        # -------------------------------------------------- #
        # -                    Widgets                     - #
        # -------------------------------------------------- #
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.console_frame = ttk.Frame(self.main_frame)
        self.console_frame['borderwidth'] = 12
        self.console_frame['relief'] = 'groove'
        self.btn_frame = ttk.Frame(self.main_frame)

        self.console_label = ttk.Label(self.console_frame, text='Console Output:')
        self.current_file = StringVar()
        self.current_label = ttk.Label(self.console_frame, textvariable=self.current_file)
        self.current_file.set('No file loaded.')
        self.console_text = Text(self.console_frame, width=70, height=20, font=self.regular_font, wrap=WORD, fg='#2c3e50', relief='groove')
        self.console_scrollbar = ttk.Scrollbar(self.console_frame, command=self.console_text.yview)
        self.console_text.config(yscrollcommand=self.console_scrollbar.set)
        self.console_text.insert(END, 'Data Parser' + (' ' * 49) + time.strftime('%m/%d/%Y'))

        self.search_input = ttk.Entry(self.console_frame, width=40)
        self.search_input.config(state=DISABLED)
        self.add_btn = ttk.Button(self.console_frame, width=10, text='Add', command=self.add_event)
        self.add_btn.config(state=DISABLED)
        self.relative_btn = ttk.Button(self.console_frame, width=10, text='Relative', command=self.relative_search_event)
        self.relative_btn.config(state=DISABLED)
        self.cont_btn = ttk.Button(self.console_frame, width=10, text='Continue', command=self.select_list_item)
        self.cont_btn.config(state=DISABLED)
        self.exact_btn = ttk.Button(self.console_frame, width=10, text='Exact', command=self.exact_search_event)
        self.exact_btn.config(state=DISABLED)
        self.detail_var = StringVar()
        self.detail_box = ttk.Label(self.console_frame, textvariable=self.detail_var)
        self.options_list = StringVar()
        self.options_box = Listbox(self.console_frame, height=8, width=50, listvariable=self.options_list, activestyle='none', selectbackground='#2ecc71', font=self.regular_font, relief='flat', highlightbackground='#95a5a6')
        self.options_scrollbar = ttk.Scrollbar(self.console_frame, command=self.options_box.yview)
        self.options_box.config(yscrollcommand=self.options_scrollbar.set)

        self.console_text.insert(END, '\n' + ('-' * 70))
        self.console_text.insert(END, '\nReady, Waiting for csv/xls/xlsx file...')
        self.console_text.config(state=DISABLED)
        self.console_text.tag_configure('green', foreground='#27ae60')
        self.console_text.tag_configure('blue', foreground='#2980b9')

        self.exit_btn = ttk.Button(self.btn_frame, width=18, text='Close Parser', command=self.close_window)
        self.open_btn = ttk.Button(self.btn_frame, width=18, text='Open Data', command=self.file_browser)
        self.save_btn = ttk.Button(self.btn_frame, width=18, text='Save to CSV', command=self.save_output)
        self.save_btn.config(state=DISABLED)


        # -------------------------------------------------- #
        # -                     Layout                     - #
        # -------------------------------------------------- #
        self.main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.console_frame.grid(column=0, row=0, sticky=N)
        self.btn_frame.grid(column=0, row=3, columnspan=3, pady=6, sticky=S)

        self.console_label.grid(column=0, row=0, sticky=W)
        self.current_label.grid(column=0, row=0, sticky=E, ipady=10)
        self.console_text.grid(column=0, row=1)
        self.console_scrollbar.grid(column=1, row=1, sticky=NS)
        self.search_input.grid(column=0, row=2, pady=2, ipady=2, columnspan=2)

        self.add_btn.grid(column=0, row=3, padx=(14, 0), pady=(0, 30), sticky=S)
        self.relative_btn.grid(column=0, row=3, padx=(166, 0), sticky=W)
        self.cont_btn.grid(column=0, row=3, padx=(14, 0), pady=(30, 0), sticky=N)
        self.exact_btn.grid(column=0, row=3, padx=(0, 150), sticky=E)

        self.detail_box.grid(column=0, row=5)
        self.options_box.grid(column=0, row=4, pady=(4, 4), columnspan=2)
        self.options_scrollbar.grid(column=1, row=4, sticky=NS)

        self.exit_btn.grid(column=2, row=0, sticky=E)
        self.open_btn.grid(column=1, row=0, padx=(20, 20))
        self.save_btn.grid(column=0, row=0, sticky=W)


        # -------------------------------------------------- #
        # -               Grid Configuration               - #
        # -------------------------------------------------- #
        self.root.columnconfigure(0, weight=3)
        self.root.rowconfigure(0, weight=3)

        self.main_frame.columnconfigure(0, weight=3)
        self.main_frame.rowconfigure(0, weight=3)
        self.main_frame.rowconfigure(1, weight=3)

        self.console_frame.columnconfigure(0, weight=3)
        self.console_frame.columnconfigure(1, weight=3)
        self.console_frame.rowconfigure(0, weight=3)
        self.console_frame.rowconfigure(1, weight=3)
        self.console_frame.rowconfigure(2, weight=3)
        self.console_frame.rowconfigure(3, weight=3)
        self.console_frame.rowconfigure(4, weight=3)
        self.console_frame.rowconfigure(5, weight=3)

        self.btn_frame.columnconfigure(0, weight=3)
        self.btn_frame.columnconfigure(1, weight=3)
        self.btn_frame.columnconfigure(2, weight=3)
        self.btn_frame.rowconfigure(0, weight=3)


        # -------------------------------------------------- #
        # -                  Key Bindings                  - #
        # -------------------------------------------------- #
        self.root.protocol('WM_DELETE_WINDOW', self.close_window)

        self.relative_btn.bind('<Enter>', lambda x: self.detail_var.set('Find all combinations with term (\'peptide\': isopeptide, neuropeptide, peptide bond...).'))
        self.relative_btn.bind('<Leave>', lambda x: self.detail_var.set(''))

        self.cont_btn.bind('<Enter>', lambda x: self.detail_var.set('Enter current selection and continue.'))
        self.cont_btn.bind('<Leave>', lambda x: self.detail_var.set(''))

        self.exact_btn.bind('<Enter>', lambda x: self.detail_var.set('Find exact term only.'))
        self.exact_btn.bind('<Leave>', lambda x: self.detail_var.set(''))

        self.add_btn.bind('<Enter>', lambda x: self.detail_var.set('Add current term to list of terms for custom pie-chart.'))
        self.add_btn.bind('<Leave>', lambda x: self.detail_var.set(''))

        self.search_input.bind('<Enter>', lambda x: self.detail_var.set('Enter search term then choose <Relative> or <Exact>.'))
        self.search_input.bind('<Leave>', lambda x: self.detail_var.set(''))

        self.options_box.bind('<Enter>', lambda x: self.detail_var.set('Left-click a selection then select <Continue>.'))
        self.options_box.bind('<Leave>', lambda x: self.detail_var.set(''))

        self.exit_btn.bind('<Enter>', lambda x: self.detail_var.set('Close the program.'))
        self.exit_btn.bind('<Leave>', lambda x: self.detail_var.set(''))

        self.open_btn.bind('<Enter>', lambda x: self.detail_var.set('Open a new dataset.'))
        self.open_btn.bind('<Leave>', lambda x: self.detail_var.set(''))
        
        self.save_btn.bind('<Enter>', lambda x: self.detail_var.set('Finish working with and save current dataset.'))
        self.save_btn.bind('<Leave>', lambda x: self.detail_var.set(''))



    # -------------------------------------------------- #
    # -                GUI Functions                   - #
    # -------------------------------------------------- #
    def close_window(self):
        """Popup message on exit attempts."""
        if messagebox.askyesno(message='Are you sure you want to quit? Any unsaved results will be lost.', title='Close Parser', icon='info'):
            self.root.destroy()
            sys.exit()


    def save_output(self):
        """Handle save output on user request."""
        # Auto create dated folders within 'results' folder
        dir_path = 'results/' + time.strftime('%m_%d_%Y') + '/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        # Open save file dialog, automatically set extension to CSV
        file_path = filedialog.asksaveasfile(mode='w', defaultextension='.csv', initialdir=dir_path)
        self.dataframe.to_csv(file_path)
        self.update_console('\n' + ('-' * 70))
        self.update_console('Data saved.', 'green')
        return self.reset_parser()


    def reset_parser(self):
        self.update_console('\n' + ('-' * 70))
        self.dataframe = ''
        self.state = ''
        self.column_choice = ''
        self.search_term = ''
        self.custom_chart_terms = []
        self.save_btn.config(state=DISABLED)
        self.options_list.set('')
        self.current_file.set('No file loaded.')
        self.update_console('Ready, Waiting for csv/xls/xlsx file...')


    def update_console(self, output, tag=None):
        """Handle text display for console widget."""
        self.console_text.config(state=NORMAL)
        self.console_text.insert(END, '\n' + output, tag)
        self.console_text.see(END)
        self.console_text.config(state=DISABLED)


    def select_list_item(self, event=None):
        """Handle selection within listbox depending on program state."""
        selection = self.options_box.curselection()
        if len(selection) > 0:
            value = self.options_box.get(selection[0])
            self.update_console(' > ' + value, 'green')
            if self.state == 'beginning':
                if value == 'Create Custom Pie-Chart':
                    self.state = 'custom_pie_chart'
                elif value == 'Create Top 20 Pie-Chart':
                    self.state = 'column_scan'
                elif value == 'Search Term':
                    self.state = 'search'
                elif value == 'Create Histogram':
                    self.state = 'histogram'
                self.pick_column()
            else:
                self.column_choice = value
                self.options_list.set('')
                if self.state == 'custom_pie_chart':
                    self.custom_term_prompt()
                elif self.state == 'column_scan':
                    self.scan_column()
                elif self.state == 'search':
                    self.term_prompt()
                elif self.state == 'histogram':
                    self.create_histogram()

    def term_prompt(self):
        """Enable entry widget, set program to wait for user search term."""
        self.update_console('\nEnter search term (e.g. \'acetylation\', \'3D-structure\')', 'blue')
        self.update_console('or numerical range (e.g. \'<1500\', \'>1e-40\')', 'blue')
        self.update_console('NOTE: For numerical search, <Relative> and <Exact> will behave the same.', 'blue')
        self.search_input.config(state=NORMAL)
        self.relative_btn.config(state=NORMAL)
        self.exact_btn.config(state=NORMAL)
        self.cont_btn.config(state=DISABLED)
        self.search_input.focus()


    def relative_search_event(self):
        """Set parser search state to 'relative'."""
        self.state = 'Relative search'
        return self.get_search_input()


    def exact_search_event(self):
        """Set parser search state to 'exact'."""
        self.state = 'Exact search'
        return self.get_search_input()


    def add_event(self):
        """Collect custom term for custom chart."""
        return self.get_search_input()


    def get_search_input(self, event=None):
        """Collect user search term while entry is enabled."""
        self.search_term = self.search_input.get()
        if self.search_term:
            if self.state == 'custom_pie_chart':
                if self.search_term.lower() != 'end':
                    self.custom_chart_terms.append(self.search_term)
                    self.update_console('Current terms: ' + str(self.custom_chart_terms), 'green')
                    self.search_input.delete(0, END)
                    self.search_input.focus()
                else:
                    self.search_input.delete(0, END)
                    self.search_input.config(state=DISABLED)
                    self.add_btn.config(state=DISABLED)
                    return self.custom_pie_chart()
            else:
                self.search_input.delete(0, END)
                self.search_input.config(state=DISABLED)
                self.relative_btn.config(state=DISABLED)
                self.exact_btn.config(state=DISABLED)
                self.update_console(' > ' + self.search_term, 'green')
                self.search_keyword()


    def custom_term_prompt(self):
        """Enable entry widget, set program to wait for custom term."""
        self.update_console('\nEnter each term followed by <Add> to create list of custom chart terms (enter \'end\' to finish)', 'blue')
        self.search_input.config(state=NORMAL)
        self.add_btn.config(state=NORMAL)
        self.cont_btn.config(state=DISABLED)
        self.search_input.focus()
            

    def file_browser(self):
        """Handle data selection by user."""
        # Open file browser, allow selection of csv/xls/xlsx only
        if len(self.dataframe) == 0:
            self.data_file = filedialog.askopenfilename(parent=self.root, filetypes=(('CSV files', '*.csv'),('Excel files', '*.xls;*.xlsx')))
            allowed_types = ('.csv', '.xls', '.xlsx')
            if self.data_file.endswith(allowed_types):
                self.dataframe = self.create_dataframe(self.data_file)
                load_message = '\nFile loaded: ' + os.path.basename(self.data_file) + ' (' + str(len(self.dataframe)) + ' rows in file)'
                self.update_console(load_message)
                self.current_file.set('File in use: ' + os.path.basename(self.data_file))
                self.save_btn.config(state=NORMAL)
                self.original_dataframe_length = len(self.dataframe)
                return self.program_begin()
            elif not self.data_file:
                return None
        else:
            # If dataframe currently loaded, confirmation to close and open new
            if messagebox.askyesno(message='Open new data? This will cause previous unsaved data to be lost.', title='Open New', icon='info'):
                self.reset_parser()
                return self.file_browser()


    def program_begin(self):
        """Greet user with initial options and set program state."""
        self.update_console('Select Parser Function', 'blue')
        self.options_list.set(('Search Term', 'Create Custom Pie-Chart', 'Create Top 20 Pie-Chart', 'Create Histogram'))
        self.cont_btn.config(state=NORMAL)
        self.state = 'beginning'



    # -------------------------------------------------- #
    # -                Parser Functions                - #
    # -------------------------------------------------- #
    def create_dataframe(self, data_file):
        """Create dataframe depending on extension type."""
        if data_file.endswith('.csv'):
            dataframe = pd.read_csv(data_file, header=0)
        elif data_file.endswith('.xls') or data_file.endswith('.xlsx'):
            dataframe = pd.read_excel(data_file, header=0)
        return dataframe


    def pick_column(self):
        """Create column headers list within dataframe, push them to listbox."""
        header_info = list(self.dataframe)
        header_message = ', '.join(list(self.dataframe))
        self.update_console('\nSelect Column of Interest', 'blue')
        self.update_console(header_message)
        self.options_list.set(tuple(header_info))


    def scan_column(self):
        """Scan for all unique elements in column."""
        total = []
        unique = []
        number_of_rows = 0
        empty_elements = 0
        for row in self.dataframe[self.column_choice]:
            if type(row) is str:
                # Remove text within parentheses (GO numbers)
                row = re.sub(r'\([^)]*\)', '', row)
                # Split string by semicolon and comma
                row_subarray = re.split(';', row)
                for element in row_subarray:
                    element = element.strip()
                    # Toss rows with empty or null data
                    if 'no_' in element.lower() or 'uncharacterized' in element.lower() or element == '':
                        empty_elements += 1
                    # Check if element is unique
                    elif element.lower() not in total:
                        unique.append(element.lower())
                        total.append(element.lower())
                    # Else add to total only
                    else:
                        total.append(element.lower())
            # If row is not string, skip row (NaN)
            else:
                pass
            number_of_rows += 1
        return self.create_graph(unique, total, number_of_rows, empty_elements)


    def custom_pie_chart(self):
        """Creation of custom pie chart. 
        User defines any number of search terms which are searched 
        and pieced into a chart relative to the whole."""
        def format_autopct(pct):
            return '{:.0f}'.format(pct * analyzed_total / 100)

        plt.rcParams['figure.figsize'] = 14, 7
        plt.rcParams['font.size'] = 10
        plt.clf()
        labels = []
        sizes = []
        colors = ['#f1c40f', '#2ecc71', '#1abc9c', '#e74c3c', '#9b59b6', '#e67e22', '#8e44ad', '#34495e', '#3498db', '#27ae60']

        number_of_rows = len(self.dataframe)
        analyzed_total = 0
        empty_elements = 0
        term_dictionary = {}
        for term in self.custom_chart_terms:
            term_dictionary[term] = 0

        for row in self.dataframe[self.column_choice]:
            if type(row) is str:
                # Remove text within parentheses (GO numbers)
                row = re.sub(r'\([^)]*\)', '', row)
                # Split string by semicolon and comma
                row_subarray = re.split(';|,', row)
                for element in row_subarray:
                    element = element.strip()
                    # Toss rows with empty or null data
                    if 'no_' in element.lower() or 'uncharacterized' in element.lower() or element == '':
                        empty_elements += 1
                    else:
                        for term in self.custom_chart_terms:
                            if term.lower() in element.lower():
                                term_dictionary[term] += 1

        # Add info from dictionary to pie-chart labels/sizes
        while len(term_dictionary) > 0:
            top = max(term_dictionary, key=term_dictionary.get)
            labels.append(top)
            sizes.append(term_dictionary[top])
            analyzed_total += term_dictionary[top]
            del term_dictionary[top]

        title = 'Custom Pie-Chart for ' + str(self.column_choice)
        subtitle = str(number_of_rows) + ' rows total | value is number of rows containing term'
        plt.text(0.0, 1.15, title, ha='center', fontsize=15)
        plt.text(0.0, 1.10, subtitle, ha='center', fontsize=11)

        plt.pie(sizes, labels=labels, colors=colors, startangle=180, labeldistance=1.03, pctdistance=0.90, autopct=format_autopct)
        plt.axis('equal')
        plt.ion()
        plt.show()
        self.update_console('\n---- Chart Output ------------------------------\n', 'green')
        return self.program_begin()


    def create_graph(self, analyzed, total, number_of_rows, empty_elements):
        """Pie chart creation and output."""
        def format_autopct(pct):
            return '{:.0f}'.format(pct * analyzed_total / 100)

        plt.rcParams['figure.figsize'] = 14, 7
        plt.rcParams['font.size'] = 10
        plt.clf()
        labels = []
        sizes = []
        colors = ['#f1c40f', '#2ecc71', '#1abc9c', '#e74c3c', '#9b59b6', '#e67e22', '#8e44ad', '#34495e', '#3498db', '#27ae60']

        analyzed_dict = {}
        analyzed_total = 0
        for element in analyzed:
            results = total.count(element)
            title = str(element)
            analyzed_dict[title] = results
        # Add top values to labels/size for pie-chart
        i = 0
        while i < 20 and len(analyzed_dict) > 0:
            top = max(analyzed_dict, key=analyzed_dict.get)
            labels.append(top)
            sizes.append(analyzed_dict[top])
            analyzed_total += total.count(top)
            del analyzed_dict[top]
            i += 1

        title = 'Top ' + str(i) + ' Results in ' + str(self.column_choice)
        subtitle = str(number_of_rows) + ' rows total | value is number of rows containing term'
        plt.text(0.0, 1.15, title, ha='center', fontsize=15)
        plt.text(0.0, 1.10, subtitle, ha='center', fontsize=11)

        plt.pie(sizes, labels=labels, colors=colors, startangle=180, labeldistance=1.03, pctdistance=0.90, autopct=format_autopct)
        plt.axis('equal')
        plt.ion()
        plt.show()
        self.update_console('\n---- Chart Output ------------------------------\n', 'green')
        return self.program_begin()


    def create_histogram(self):
        """Histogram creation and output."""
        plt.rcParams['figure.figsize'] = 14, 7
        plt.rcParams['font.size'] = 10
        plt.clf()
        df_values = []
        tossed = 0
        if self.column_choice == 'ContigLength':
            for row in self.dataframe[self.column_choice]:
                if row > 400 and row < 4001:
                    df_values.append(row)
                else:
                    tossed += 1
            bins = [0, 201, 401, 601, 801, 1001, 1201, 1401, 1601, 1801, 2001, 2201, 2401, 2601, 2801, 3001, 3201, 3401, 3601, 3801, 4001]
            plt.xticks(range(0, 4000, 200))
            plt.xlim([0, 4000])
        else:
            for row in self.dataframe[self.column_choice]:
                if type(row) in (str, list):
                    self.update_console('\nHistogram creation only possible for columns containing numerical values.')
                    return self.program_begin()
                else:
                    df_values.append(row)
            bins = 20
            plt.xlim([0, max(df_values)])

        n, bins, patches = plt.hist(df_values, bins=bins, facecolor='green', alpha=0.5)
        df_range = str(min(df_values)) + ' - ' + str(max(df_values))
        df_mean = round(np.mean(df_values), 2)
        df_median = round(np.median(df_values), 2)
        df_std = round(np.std(df_values), 2)
        df_total = len(df_values)

        plt.title('Histogram of ' + str(self.column_choice) + ' (' + str(df_total) + ' total)', fontsize=16)
        plt.suptitle('Standard Deviation: ' + str(df_std) + ', Mean: ' + str(df_mean) + ', Median: ' + str(df_median) + ', Range: ' + df_range, fontsize=12)

        plt.xlabel(str(self.column_choice))
        plt.ylabel('Rows')
        plt.ion()
        plt.show()
        self.update_console('\n---- Histogram Output --------------------------\n', 'green')
        return self.program_begin()


    def search_keyword(self):
        """Return all rows with term in specified column."""
        row_index = -1
        row_list = []
        search_results = 0
        for row in self.dataframe[self.column_choice]:
            row_index += 1

            # Rows with numerical values check for values within range
            if 'numpy' in str(type(row)) or type(row) in (float, int):
                # Test for NaN
                if row != row:
                    pass
                elif self.search_term[0] == '>' and float(self.search_term[1:]) <= row:
                    search_results += 1
                    row_list.append(row_index)
                elif self.search_term[0] == '<' and float(self.search_term[1:]) >= row:
                    search_results += 1
                    row_list.append(row_index)
                elif self.search_term[0] == '=' and float(self.search_term[1:]) == row:
                    search_results += 1
                    row_list.append(row_index)
                elif self.search_term[0] not in ('<', '>', '='):
                    self.update_console('\nNumerical values require < or > to specify range.')
                    return self.term_prompt()

            # Rows composed of strings split and check elements, regex
            elif type(row) is str:
                row_subarray = re.split(';', row)
                for element in row_subarray:
                    if self.state == 'Relative search':
                        if re.search('(?i)' + self.search_term, element):
                            search_results += 1
                            row_list.append(row_index)
                    elif self.state == 'Exact search':
                        if re.match('(?i)' + self.search_term, element):
                            search_results += 1
                            row_list.append(row_index)
            else:
                print(type(row), 'unexpected.')

        # Update console/dataframe
        if search_results > 0:
            self.update_console('\n' + self.state + ' [' + str(search_results) + ' results found for \'' + self.search_term + '\' in \'' + self.column_choice + '\']')
            searched_data = []
            for index in row_list:
                searched_data.append(self.dataframe.irow(index))
            self.dataframe = pd.DataFrame(data=searched_data)
            self.update_console('\tDataframe updated (' + str(len(self.dataframe)) + ' rows, original was ' + str(self.original_dataframe_length) + ' rows)\n')
        else:
            self.update_console('\n' + self.state + ' [No results found for \'' + self.search_term + '\' in \'' + self.column_choice + '\']')

        # Reset choices and go to beginning of program with updated dataframe
        self.column_choice = ''
        self.search_term = ''
        self.custom_chart_terms = []
        return self.program_begin()






def create_interface():
    """Initialize GUI root; set dimensions and properties."""
    root = Tk()
    root.title('Data Parser')
    screen_x = root.winfo_screenwidth()
    screen_y = root.winfo_screenheight()
    window_x, window_y = 640, 660
    x_pos = (screen_x / 2) - (window_x / 2)
    y_pos = (screen_y / 2) - (window_y / 2) - 30
    root.geometry('%dx%d+%d+%d' % (window_x, window_y, x_pos, y_pos))
    root.resizable(FALSE, FALSE)
    return root


def main():
    root = create_interface()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()