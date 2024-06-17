from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput 
from kivy.uix.button import Button 
from pypdf import PdfWriter

import os

Builder.load_file('main_design.kv')

class MyLayout(Widget):

    def selected(self, filename):   #Display the recently selected file to the console
        
        try:
            print(filename[-1])
        except:
            print("Error Selecting File")

    def selection_button_pressed(self, filename): #Display all selected files
        print("Selected:" , filename)

    def merge_button_pressed(self, filename):
        
        if not filename: 
            return
        
        try:
            for path in filename:
                file_path = os.path.dirname(path)
        except:
            print("Error")
            return
        
        ## Popup to enter a name for the merged PDF ##
        layout = GridLayout(cols = 1, padding = 10) 
        popup_buttons = GridLayout(cols = 2, size_hint = (1, 0.2)) 
        text_input = TextInput(size_hint = (1, 0.2)) 
        save_button = Button(text = "Save")
        close_button = Button(text = "Close") 

        layout.add_widget(text_input) 
        popup_buttons.add_widget(save_button)
        popup_buttons.add_widget(close_button)  
        layout.add_widget(popup_buttons)      
        
        popup = Popup(title = "Enter new filename", content = layout, size_hint =(.75, .3))   
        popup.open()    
  
        save_button.bind(on_press=lambda *args: self.savename_and_merge(text_input.text, file_path, filename))
        close_button.bind(on_press = popup.dismiss)

        print("Merged and saved as " , filename)

    def savename_and_merge(self, new_filename, file_path, pdfs_array):
        
        # Prevent illegal characters in files such as: * " / \ < > : | ? Limits filenames to these ASCII characters
        allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"

        if not new_filename: 
            print("Nothing Here")
            return
        
        # Sanitizing User Input: Make sure the filename doesn't contain any illegal characters
        valid_name = ''
        for char in new_filename:
            if char in allowed_chars:
                valid_name += char
            else:
                valid_name += '_'
        valid_name += '.pdf'

        #Place the merged pdf into the directory of the last selected file
        full_path = os.path.join(file_path, valid_name)
        self.merge_pdf_files(pdfs_array, full_path)
        print(full_path)

    #Deselect all selected pdfs
    def cancel_button_pressed(self):
        self.ids.filechooser.selection = []

    def merge_pdf_files(self, pdf_files, full_path):

        merger = PdfWriter()

        for pdf in pdf_files:
            merger.append(pdf)

        merger.write(full_path)
        merger.close()
        
class MergeDocApp(App):
    def build(self):

        from kivy import Config
        Config.set('input', 'mouse', 'mouse,disable_multitouch')
        return MyLayout()
    
if __name__ == '__main__':
    MergeDocApp().run()