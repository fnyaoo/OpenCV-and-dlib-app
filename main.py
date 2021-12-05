from tkinter import *
from PIL import ImageTk, Image
import cv2
import tkinter.filedialog as tkFileDialog
from tkinter.colorchooser import askcolor
import dlib
import logging.config
from tkinter import messagebox as mb


# path of file

def openfn():
    global path, cpath
    path = tkFileDialog.askopenfilename()
    if path:
        cpath = path
        logger.info("Выбрана и загруженна фотография.")
        proc_img()
    else:
        path = cpath
        logger.error("Ошибка! Фотография не была выбрана!")


# proc on img

def proc_img():
    global img1
    # load the image from disk
    image = cv2.imread(path)

    # convert it to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        face_landmarks = predictor(gray, face)
        for n in range(36, 42):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            cv2.circle(image, (x, y), 1, (b, g, r), 5)

    #  represents images in BGR order
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img1 = image

    logger.info("Фотография обработана.")
    print_img()


# print img to window

def print_img():
    image = img1
    global lmain, flag
    flag = True
    if flag is True:
        web_btn.configure(state=NORMAL)

    # scale image
    scale_percent = 35
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    # convert the images to PIL format
    resized = Image.fromarray(resized)

    # and then to ImageTk format
    resized = ImageTk.PhotoImage(resized)

    # if the panels are None, initialize them
    if lmain is None:
        lmain = Label(image=resized)
        lmain.image = resized
        lmain.pack(padx=10, pady=10, anchor=N)
    else:
        # update the panels
        lmain.destroy()
        lmain = Label(image=resized)
        lmain.configure(image=resized)
        lmain.image = resized
        lmain.pack(padx=10, pady=10, anchor=N)

    logger.info("Обработанная фотография вывелась на экран.")


# show web

def show_frame():
    global lmain, imgtk, flag, frame

    if flag is True or flag is None:
        logger.info("Запустилась веб-камера.")

    flag = False

    # disable button
    if not flag:
        web_btn.configure(state=DISABLED)

    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(img_gray)
    for face in faces:
        face_landmarks = predictor(img_gray, face)
        for n in range(36, 42):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            cv2.circle(frame, (x, y), 1, (b, g, r), 1)

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)

    if lmain is None:
        lmain = Label(image=imgtk)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(10, show_frame)
        lmain.pack(padx=10, pady=10, anchor=N)
    else:
        lmain.configure(image=imgtk)
        lmain.image = imgtk
        lmain.after(10, show_frame)


# save img

def save_file():
    global filename
    if flag is True:
        img = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
        filename = tkFileDialog.asksaveasfile(mode='w', defaultextension=".jpg")

        if filename:
            cv2.imwrite(filename.name, img)
            logger.info("Обработанная фотография была сохранена.")
        else:
            logger.error("Ошибка! Окно с сохранением было закрыто, фотография не была сохранена!")

    elif flag is False:
        filename = tkFileDialog.asksaveasfile(mode='w', defaultextension=".jpg")

        if filename:
            cv2.imwrite(filename.name, frame)
            logger.info("Скриншот с веб-камеры был сохранен.")
        else:
            logger.error("Ошибка! Окно с сохранением было закрыто, скриншот не был сохранен!")

    else:
        mb.showinfo("Ошибка", "Сначала откройте фотографию или веб-камеру!")
        logger.error("Ошибка! Была совершена попытка сохранить файл, но никакая функция не обрабатывалась!")


# color chooser

def color_chooser():
    global r, g, b, color
    color = askcolor(title="Выберите цвет...")

    if color[1] is None:
        logger.error("Ошибка! Окно с выбором цвета было закрыто, цвет не был изменён!")

    else:
        color_btn['bg'] = color[1]
        h = color[1].lstrip('#')
        rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]

        if flag is True:
            logger.info("Выбран цвет для обработки на фотографии.")
            proc_img()
        else:
            logger.info("Выбран цвет для обработки на веб-камере.")


# window part

# Load the detector
detector = dlib.get_frontal_face_detector()
# Load the predictor
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# logger

dictLogConfig = {
    "version": 1,
    "handlers": {
        "fileHandler": {
            "class": "logging.FileHandler",
            "formatter": "myFormatter",
            "filename": "log_file.log"
        }
    },
    "loggers": {
        "OpenCV_App": {
            "handlers": ["fileHandler"],
            "level": "INFO",
        }
    },
    "formatters": {
        "myFormatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    }
}

logging.config.dictConfig(dictLogConfig)
logger = logging.getLogger("OpenCV_App")
logger.info("***** Программа запустилась! *****")

r = 0
g = 255
b = 0

flag = None
lmain = None
path = None
cpath = None
color = None
filename = None

root = Tk()
root.title("Вилданова К. ПРИ-О-17/1")
root.geometry("720x540")
root.resizable(width=False, height=False)

# web cam settings
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

# buttons
photo_btn = Button(root, text="Выбрать фото", command=openfn)
photo_btn.pack(fill=X, padx="10", pady="5", anchor=N)

web_btn = Button(root, text="Открыть веб-камеру", command=show_frame)
web_btn.pack(fill=X, padx="10", pady="5", anchor=N)

save_btn = Button(root, text="Сохранить изображение", command=save_file)
save_btn.pack(fill=X, padx="10", pady="5", anchor=N)

color_btn = Button(root, text="Выберите цвет", command=color_chooser, bg='#00ff00')
color_btn.pack(fill=X, padx="10", pady="5", anchor=N)

root.mainloop()
