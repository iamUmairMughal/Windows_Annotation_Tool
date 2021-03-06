import tkinter
from tkinter import *
import PIL
from PIL import ImageTk, Image
from tkinter import filedialog
from os import listdir
import numpy as np
from functools import partial
from xmls import create_xml


class LabelingApp(tkinter.Tk):

    def __init__(self):
        tkinter.Tk.__init__(self)
        self.x = self.y = 0
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.label = ""
        self.files = ""

        self.shape_cor = []
        self.images ={}
        self.auto_save = BooleanVar()

        self.C = tkinter.Canvas(self)
        menuButtons = Frame(self.C)

        self.PASCAL = "PASCAL"
        self.YOLO = "YOLO"

        open_file_btn = Button(menuButtons, text="Open File", command=self.open_img)
        open_file_btn.grid(row=0, column=0, padx=5, pady=5)

        open_folder_btn = Button(menuButtons, text="Open Folder", command=self.open_folder)
        open_folder_btn.grid(row=0, column=1, padx=5, pady=5)

        self.ann_format_Button = Button(menuButtons, width=8, text=self.PASCAL, command=self.switch)
        self.ann_format_Button.grid(row=0, column=2, padx=5, pady=5)

        save_ann_Button = Button(menuButtons, text='Save Annotation', command=self.save_file)
        save_ann_Button.grid(row=0, column=3, padx=5, pady=5)

        self.auto_save_button = Checkbutton(menuButtons, text="Auto Save", variable=self.auto_save,
                 onvalue=True, offvalue=False)
        self.auto_save_button.grid(row=0, column=4, padx=5, pady=5)

        menuButtons.grid(row=0, sticky=NW)

        self.C.grid(row=0, columnspan=2, sticky=NW)

        self.C1 = tkinter.Canvas(self, height=600)
        sideButtons = Frame(self.C1)

        self.shape = StringVar(sideButtons, 'rect')

        self.shape_img1 = tkinter.PhotoImage(file='Rect.png')
        self.shape_img2 = tkinter.PhotoImage(file='Circle.png')
        self.shape_img3 = tkinter.PhotoImage(file='Line.png')
        self.shape_img4 = tkinter.PhotoImage(file='Polygon.png')

        values = {
            self.shape_img1: 'rect',
            self.shape_img2: 'circle',
            self.shape_img3: 'line',
            self.shape_img4: 'poly'
        }

        for i, (img, value) in enumerate(values.items()):
            if i < 2:
                Radiobutton(sideButtons, bg="white", image=img, variable=self.shape,
                            value=value, indicator=0, height=50, width=50).grid(row=i, column=0, padx=5, pady=5, sticky=W)
            else:
                Radiobutton(sideButtons, bg="white", image=img, variable=self.shape,
                            value=value, indicator=0, height=50, width=50).grid(row=i-2, column=1, padx=5, pady=5, sticky=W)

        next_btn = Button(sideButtons, text="Next", width=8, command=self.next_img)
        next_btn.grid(row=2, column=0, padx=5, pady=5, sticky=NW)

        previous_btn = Button(sideButtons, text="Previous", width=8, command=self.prv_img)
        previous_btn.grid(row=2, column=1, padx=5, pady=5, sticky=NW)

        self.scrollbar = Scrollbar(sideButtons)
        self.scrollbar.grid(row=3, column=0, padx=5, pady=5)
        self.mylist = Listbox(sideButtons, height=25, width=25, yscrollcommand=self.scrollbar.set)
        self.mylist.grid(row=3, rowspan=4, columnspan=2, padx=5, pady=5)

        sideButtons.grid(row=0, column=0,  padx=5, sticky=NW)

        self.C1.grid(row=1, column=0, sticky=NW)

        

        self.is_PASCAL = True

        self.C2 = tkinter.Canvas(self, width=720, height=600, cursor='cross')
        self.image_drawed = False
        self.image = np.ones((600, 720, 3), np.uint8)
        self.image.fill(255)
        self.tk_im = ImageTk.PhotoImage(image=PIL.Image.fromarray(self.image))
        self.canvas_image = self.C2.create_image(self.tk_im.width() / 2, self.tk_im.height() / 2,
                                                 anchor=CENTER)

        self.C2.tag_bind(self.canvas_image, '<Button-1>', self.on_button_press)
        self.C2.tag_bind(self.canvas_image, '<Button1-Motion>', self.on_move_press)
        self.C2.tag_bind(self.canvas_image, '<ButtonRelease-1>', self.on_button_release)

        # self.bind('w', self.start_annotate)

        self.bind('d', self.next_img)
        self.bind('a', self.prv_img)
        self.bind('<Delete>', self.dell_object)

        self.C2.grid(row=1, column=1, padx=5, pady=5)

        
        self.ScrollBar_Display()


    def clear_canvas(self):
        self.C2.delete('all')
        self.image_drawed = False
        self.image = np.ones((600, 720, 3), np.uint8)
        self.image.fill(255)
        self.tk_im = ImageTk.PhotoImage(image=PIL.Image.fromarray(self.image))
        self.canvas_image = self.C2.create_image(self.tk_im.width() / 2, self.tk_im.height() / 2,
                                                 anchor=CENTER)

        self.C2.tag_bind(self.canvas_image, '<Button-1>', self.on_button_press)
        self.C2.tag_bind(self.canvas_image, '<Button1-Motion>', self.on_move_press)
        self.C2.tag_bind(self.canvas_image, '<ButtonRelease-1>', self.on_button_release)

    def dell_object(self, event):
        self.C2.delete(self.current)
        if self.current > 2:
            del self.shape_cor[(self.current-2)]
        else:
            del self.shape_cor[0]
        # print(self.shape_cor)

    def openfilename(self):
        filename = filedialog.askopenfilename(title='Open Image')
        return filename

    def open_img(self):
        file = self.openfilename()
        self.files = [file.split('/')[-1]]

        self.folder = file[ : -(len(self.files[0])+1)]

        # print(self.files)
        # print(self.folder)

        for i in self.files:
            self.images[i] = []

        self.ScrollBar_Display()
        self._draw_image(file)

    def openfoldername(self):
        filename = filedialog.askdirectory(title='Open Folder')
        return filename

    def open_folder(self):
        self.folder = self.openfoldername()
        self.files = listdir(self.folder)
        final_files = []

        for file in self.files:
            if file.endswith((".jpg", ".png", ".jpeg")):
                final_files.append(file)
                self.images[file] = []

        self.files = final_files
        final_files = []

        self.ScrollBar_Display()
        self._draw_image(self.folder+'/'+self.files[0])

    def switch(self):
        if self.is_PASCAL:
            self.ann_format_Button.config(text=self.YOLO)
            self.is_PASCAL = False
        else:
            self.ann_format_Button.config(text=self.PASCAL)
            self.is_PASCAL = True

    def ScrollBar_Display(self):
        self.mylist.delete(0,'end')

        for file in self.files:
            self.mylist.insert(END, file)
        self.scrollbar.config(command=self.mylist.yview)

    def _draw_image(self, file):
        self.image_drawed = True
        image = PIL.Image.open(file)
        self.img = image

        self.img_width, self.img_height = image.size

        self.current_img_name = file
        self.current_img_index = self.files.index(self.current_img_name.split('/')[-1])


        if self.img_width > 720 or self.img_height > 600:
            self.img.thumbnail((720, 600))

        img_width2, img_height2 = self.img.size
        y_factor, x_factor = self.img_height / img_height2, self.img_width / img_width2

        rects = self.images.get(self.current_img_name.split('/')[-1])

        if len(rects) !=0:
            for rect in rects:
                # self.shape_cor.append(rect)
                rect[0] = int(rect[0] / x_factor)
                rect[1] = int(rect[1] / y_factor)
                rect[2] = int(rect[2] / x_factor)
                rect[3] = int(rect[3] / y_factor)

                rect[0] = int(rect[0] + ((720 / 2) - (img_width2 / 2)))
                rect[1] = int(rect[1] + ((600 / 2) - (img_height2 / 2)))
                rect[2] = int(rect[2] + ((720 / 2) - (img_width2 / 2)))
                rect[3] = int(rect[3] + ((600 / 2) - (img_height2 / 2)))

                # self.create_shape()

        self.tk_im = ImageTk.PhotoImage(image=self.img)
        self.C2.itemconfig(self.canvas_image, image=self.tk_im)

    def create_shape(self):

        if self.shape.get() == 'rect':
            self.current = self.C2.create_rectangle(*self.start, *self.start, width=2,
                                           outline="yellow", fill='yellow', stipple='gray12')
        elif self.shape.get() == 'circle':
            self.current = self.C2.create_oval(*self.start, *self.start, width=2,
                                               outline="yellow", stipple='gray12')
        # elif self.shape.get() == 'poly':
        #     self.current = self.C2.create_polygon(*self.start, *self.start, width=2)

    def on_button_press(self, event):

        if self.image_drawed:
            self.start = event.x, event.y

            self.create_shape()
            # self.current = self.C2.create_polygon(*self.start, *self.start, width=2)


            self.C2.tag_bind(self.current, '<Button-1>', partial(self.on_click_rectangle, self.current))
            self.C2.tag_bind(self.current, '<Button1-Motion>', self.on_move_press)
            self.C2.tag_bind(self.current, '<ButtonRelease-1>', self.on_button_release)


    def on_click_rectangle(self, tag, event):

        self.current = tag
        x1, y1, x2, y2 = self.C2.coords(tag)

        if abs(event.x-x1) < abs(event.x-x2):
            x1, x2 = x2, x1

        if abs(event.y-y1) < abs(event.y-y2):
            y1, y2 = y2, y1

        self.start = x1, y1

    def on_move_press(self, event):

        self.points = []

        if self.image_drawed:
            # For B1
            if (event.y < ((600 / 2) - (self.tk_im.height() / 2))
                    and event.x < ((720 / 2) - (self.tk_im.width() / 2))):
                self.C2.coords(self.current, *self.start,
                               ((720 / 2) - (self.tk_im.width() / 2)),
                               ((600 / 2) - (self.tk_im.height() / 2)))

            # For B2
            elif (event.y < ((600 / 2) - (self.tk_im.height() / 2))
                    and event.x > ((720 / 2) + (self.tk_im.width() / 2))):
                self.C2.coords(self.current, *self.start,
                               ((720 / 2) + (self.tk_im.width() / 2)),
                               ((600 / 2) - (self.tk_im.height() / 2)))
            # For B3
            elif (event.y > ((600 / 2) + (self.tk_im.height() / 2))
                  and event.x < ((720 / 2) - (self.tk_im.width() / 2))):
                self.C2.coords(self.current, *self.start,
                               ((720 / 2) - (self.tk_im.width() / 2)),
                               ((600 / 2) + (self.tk_im.height() / 2)))

            # For B4
            elif (event.y > ((600 / 2) + (self.tk_im.height() / 2))
                  and event.x > ((720 / 2) + (self.tk_im.width() / 2))):
                self.C2.coords(self.current, *self.start,
                               ((720 / 2) + (self.tk_im.width() / 2)),
                               ((600 / 2) + (self.tk_im.height() / 2)))


            # Inko Last Tk Ni Cherna

            elif (event.y > ((600 / 2) + (self.tk_im.height() / 2))
                  and event.x < ((720 / 2) + (self.tk_im.width() / 2))):
                self.C2.coords(self.current, *self.start,
                               event.x,
                               ((600 / 2) + (self.tk_im.height() / 2)))

            elif (event.y < ((600 / 2) + (self.tk_im.height() / 2))
                  and event.x > ((720 / 2) + (self.tk_im.width() / 2))):
                self.C2.coords(self.current, *self.start,
                               ((720 / 2) + (self.tk_im.width() / 2)),
                               event.y)
            elif (event.y > ((600 / 2) - (self.tk_im.height() / 2))
                  and event.x < ((720 / 2) - (self.tk_im.width() / 2))):
                self.C2.coords(self.current, *self.start,
                               ((720 / 2) - (self.tk_im.width() / 2)),
                               event.y)
            elif (event.y > ((600 / 2) + (self.tk_im.height() / 2))
                  and event.x < ((720 / 2) - (self.tk_im.width() / 2))):
                self.C2.coords(self.current, *self.start,
                               ((720 / 2) - (self.tk_im.width() / 2)),
                               ((600 / 2) + (self.tk_im.height() / 2)))
            elif (event.y < ((600 / 2) - (self.tk_im.height() / 2))
                  and event.x > ((720 / 2) - (self.tk_im.width() / 2))):
                self.C2.coords(self.current, *self.start,
                               event.x,
                               ((600 / 2) - (self.tk_im.height() / 2)))
            else:
                self.C2.coords(self.current, *self.start, event.x, event.y)

            # self.points = []

            self.points.append(int(self.start[0]))
            self.points.append(int(self.start[1]))
            self.points.append(int(event.x))
            self.points.append(int(event.y))

    def save_file(self):
        # self.images[self.current_img_name.split('/')[-1]] = [self.shape, self.label, self.shape_cor]

        create_xml(self.folder, self.current_img_name.split('/')[-1],
                   self.folder + '/' + self.current_img_name.split('/')[-1],
                   (self.img_width, self.img_height, 3),
                   self.shape_cor)

    def save_label(self):

        if self.E1.get() != "":
            # self.label = self.E1.get()
            self.new_Points.append(self.E1.get())
            self.new_Points.append(self.shape.get())

            self.C2.create_text(self.x, self.y, text=self.new_Points[4], fill="yellow")

            self.label_window.destroy()
        else:
            print('Set label First!')

    def exit_label_window(self):
        if self.E1.get() !="":
            self.label_window.destroy()

    def create_label_window(self):

        self.label_window = Toplevel(self)
        self.label_window.title('Label')
        self.label_window.overrideredirect(0)
        box_Frame = Frame(self.label_window, relief=RIDGE)

        rh = self.winfo_x()
        rw = self.winfo_y()

        self.label_window.geometry('+%d+%d' % (rw + 100, rh + 100))

        L1 = Label(box_Frame, text="Label: ")

        L1.grid(row=0, column=0)
        self.E1 = Entry(box_Frame)
        self.E1.grid(row=0, column=1)

        OK_btn = Button(box_Frame, text='OK', command=self.save_label).grid(row=1, column=0)
        cancel_btn = Button(box_Frame, text='Cancel', command=self.exit_label_window).grid(row=1, column=1)

        box_Frame.grid(row=0,column=0)

    def on_button_release(self, event):

        if self.image_drawed:
            self.new_Points = self.points

            if len(self.new_Points) == 4:

                self.create_label_window()

                self.x = self.new_Points[0] + 10
                self.y = self.new_Points[1] - 10

                self.new_Points[0] = int(self.points[0] - ((720 / 2) - (self.tk_im.width() / 2)))
                self.new_Points[1] = int(self.points[1] - ((600 / 2) - (self.tk_im.height() / 2)))
                self.new_Points[2] = int(self.points[2] - ((720 / 2) - (self.tk_im.width() / 2)))
                self.new_Points[3] = int(self.points[3] - ((600 / 2) - (self.tk_im.height() / 2)))

                h2 = self.tk_im.height()
                w2 = self.tk_im.width()

                w1, h1 = self.img_width, self.img_height
                y_factor, x_factor = h1/h2, w1/w2

                self.new_Points[0] = int(self.new_Points[0] * x_factor)
                self.new_Points[1] = int(self.new_Points[1] * y_factor)
                self.new_Points[2] = int(self.new_Points[2] * x_factor)
                self.new_Points[3] = int(self.new_Points[3] * y_factor)

                if len(self.shape_cor) > (self.current-2):
                    self.shape_cor[(self.current-2)] = self.new_Points
                else:
                    self.shape_cor.append(self.new_Points)

    def next_img(self,event= ''):

        if self.current_img_index != (self.mylist.size()-1):
            next_img_name = self.folder+'/'+self.mylist.get(
                self.current_img_index+1
            )

            self.images[self.current_img_name.split('/')[-1]] = self.shape_cor

            if self.auto_save.get():
                self.save_file()

            self.shape_cor = []
            self.label = ""

            self.clear_canvas()
            self._draw_image(next_img_name)

    def prv_img(self,event= ''):

        if self.current_img_index != 0:
            prv_img_name = self.folder + '/' + self.mylist.get(
                self.current_img_index -1
            )

            self.images[self.current_img_name.split('/')[-1]] = self.shape_cor

            if self.auto_save.get():
                self.save_file()
            self.shape_cor = []
            self.label = ""

            self.clear_canvas()
            self._draw_image(prv_img_name)

if __name__ == "__main__":
    app = LabelingApp()
    app.mainloop()
