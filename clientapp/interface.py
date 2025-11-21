import customtkinter as ctk
from customtkinter import *
import threading

from clientapp import getStatus
import script
import indexscript
import getPosision
import config
import os
import getGraphs

import getLocalHost
from PIL import Image
from getLocalHost import send_loop, receive_loop

app = CTk()
app.geometry('1000x700')
app.title('DSA-Domowy System Automatyzacji')
app.configure(fg_color = '#666666')
framedwa = CTkFrame(master=app,
                    fg_color="#434343",
                    border_color="#434343",
                    border_width=1,
                    height=72)
framedwa.pack(side="top",fill="x", padx=10, pady=(10,0))
frame = CTkFrame(master=app,
                 fg_color="#434343",
                 border_color="#434343",
                 border_width=1,
                 width=120,
                 height=190)
frame.pack(padx=0, pady=(50,0))
frametrzy = CTkFrame(master=app,
                     fg_color="#434343",
                     border_color="#434343",
                     border_width=1,
                     width=120,
                     height=190)
#frametrzy.pack( padx=10, pady=(5,0))

def switch_event():
    print("switch toggled, current value:", switch_var.get())
    config.lampa_mode = (switch_var.get()=="on")

def switch_event_two():
    print("switch toggled, current value:", switch_var_two.get())
    config.ledy_mode = (switch_var_two.get()=="on")

#przelacznik numer jeden
def switch_event_track():
    if switch_var_track.get() == "on":
        if not getPosision.runingtrack:
            threading.Thread(target=getPosision.run_main, daemon=True).start()
    elif switch_var_track.get() == "off":
        getPosision.runingtrack = False

switch_var_track = ctk.StringVar(value="off")
switch_getposision = ctk.CTkSwitch(master=framedwa,
                                   text="tracker",
                                   variable=switch_var_track,
                                   command=switch_event_track,
                                   onvalue="on",
                                   offvalue="off",
                                   button_color="#F4CCCC",
                                   progress_color="#EA9999"
                                   )
switch_getposision.place(x=140, y=20)
def switch_event_asys():
    if switch_var_asys.get() == "on":
        #if not script.runing:
        threading.Thread(target=script.run_prog, daemon=True).start()
    elif switch_var_asys.get() == "off":
        script.runing = False
        print("program off")
switch_var_asys = ctk.StringVar(value="off")
switch_asys = ctk.CTkSwitch(master=framedwa,
                            text="Asystent",
                            command=switch_event_asys,
                            variable=switch_var_asys,
                            onvalue="on",
                            offvalue="off",
                            button_color="#F4CCCC",
                            progress_color="#EA9999",
                            )
switch_asys.place(x=20, y=20)
switch_var = ctk.StringVar(value="off")
switch = ctk.CTkSwitch(master=frame,
                       text="lamp",
                       command=switch_event,
                       variable=switch_var,
                       onvalue="on",
                       offvalue="off",
                       button_color=("#F4CCCC","#F4CCCC"),
                       progress_color=("#EA9999","#EA9999"))
switch.place(x=20,y=10)

def getnetwork():
    getGraphs.network_status()

button = CTkButton(master=app,command=getnetwork,
                   text="net stat",
                   fg_color="#666666",
                   text_color="#F4CCCC",
                   width=40,
                   )
button.pack()

#przelacznik numer dwa
switch_var_two = ctk.StringVar(value="off")
switch_two = ctk.CTkSwitch(master=frame,
                           text="gniazdo 1",
                           command=switch_event_two,
                           variable=switch_var_two,
                           onvalue="on",
                           offvalue="off",
                           button_color=("#F4CCCC","#F4CCCC"),
                           progress_color=("#EA9999","#EA9999")
                           )
switch_two.place(x=20,y=80)

def segmented_button_callback(value):
    print("segmented button clicked:", value)
    if segmented_button_var.get() == "up":
        config.motor_up_state = True
        config.motor_down_state = False
    elif segmented_button_var.get() == "down":
        config.motor_up_state = False
        config.motor_down_state = True
    elif segmented_button_var.get() == "off":
        config.motor_up_state = False
        config.motor_down_state = False
    print(f"up: {config.motor_up_state}, DOWN: {config.motor_down_state}")

segmented_button_var = ctk.StringVar(value="off")
segmented_button = ctk.CTkSegmentedButton(master=app,
                                           values=["down", "off", "up"],
                                           selected_color = "#F4CCCC",
                                           command=segmented_button_callback,
                                           variable=segmented_button_var)

segmented_button.set("off")
segmented_button.place(x=20, y=200)

def sliderdwa_val(value):
    config.volume_val = float(value)
sliderdwa = CTkSlider(master=framedwa,
                      command=sliderdwa_val,
                      orientation="horizontal",
                      from_= 0,
                      to = 1,
                      width=100,
                      button_color=("#F4CCCC","#F4CCCC"),
                      progress_color=("#EA9999","#EA9999"))
sliderdwa.place(x=240,y=25)
sliderdwa.set(config.volume_val)
sliderdwa_label = CTkLabel(master=framedwa,
                           text="Volume"
                           )
sliderdwa_label.place(x=350,y=20)

#slider.place(x=20,y=200)
switch_var_index = ctk.StringVar(value="off")
def reset_index():
    if switch_var_index.get() == "on":
        indexscript.delete_and_update_index()
        if os.path.exists(indexscript.INDEX_FILE):
            switch_index.toggle()
switch_index = CTkSwitch(master=framedwa,
                         text="index reset",
                         command= reset_index,
                         variable=switch_var_index,
                         onvalue="on",
                         offvalue="off",
                         button_color=("#F4CCCC", "#F4CCCC"),
                         progress_color=("#EA9999", "#EA9999")

                         )
def open_cmd():
    current_file = os.path.abspath(__file__)
    os.system(current_file)
button_cmd = CTkButton(master=framedwa,
                       text="cmd",
                       command=open_cmd,
                       fg_color="#666666",
                       text_color="#F4CCCC",
                       width=40,
                       )
button_cmd.place(x=530,y=20)
switch_index.place(x=400,y=20)
return_command_switch_var = ctk.StringVar(value="on")

def enable_or_disable_return_command():
    if return_command_switch_var.get() == "off":
        config.return_command_mode = False
    elif return_command_switch_var.get() == "on":
        config.return_command_mode = True

return_command_switch = CTkSwitch(master=framedwa,
                                  text="voice e/d",
                                  command=enable_or_disable_return_command,
                                  variable=return_command_switch_var,
                                  onvalue="on",
                                  offvalue="off",
                                  button_color=("#F4CCCC", "#F4CCCC"),
                                  progress_color=("#EA9999", "#EA9999"))
return_command_switch.place(x=600,y=20)

#-
gniazdo2_switch_var = ctk.StringVar(value="off")

def gniazdo2_command():
    print("gniazdo2:", gniazdo2_switch_var.get())
    config.gniazdo2_mode = (gniazdo2_switch_var.get() == "on")

gniazdo2_switch = ctk.CTkSwitch(master=frame,
                                  text="voice e/d",
                                  command=gniazdo2_command,
                                  variable=gniazdo2_switch_var,
                                  onvalue="on",
                                  offvalue="off",
                                  button_color=("#F4CCCC", "#F4CCCC"),
                                  progress_color=("#EA9999", "#EA9999"))
gniazdo2_switch.place(x=20,y=150)

#-

def update_motor_mode():
    if config.motor_up_state and not config.motor_down_state:
        segmented_button_var.set("up")
    elif config.motor_down_state and not config.motor_up_state:
        segmented_button_var.set("down")
    elif not config.motor_up_state and not config.motor_down_state:
        segmented_button_var.set("off")

def update_switch_from_lampa_mode():
    if config.lampa_mode:
        switch_var.set("on")
    else:
        switch_var.set("off")
def update_switch_from_ledy_mode():
    if config.ledy_mode:
        switch_var_two.set("on")
    else:
        switch_var_two.set("off")
def update_gniazdo2():
    if config.gniazdo2_mode:
        gniazdo2_switch_var.set("on")
    else:
        gniazdo2_switch_var.set("off")


image_path = "qrcode1.png"
pil_image = Image.open(image_path)
ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(200, 200))
image_label = ctk.CTkLabel(master=app, image=ctk_image, text="")
image_label.pack(pady=10)


def periodic_check():
    if (config.motor_up_state and segmented_button_var.get() != "up") or (config.motor_down_state and segmented_button_var.get() != "down") or (not config.motor_up_state and segmented_button_var.get() != "off") or (not config.motor_down_state and segmented_button_var.get() != "off"):
        update_motor_mode()
    if (config.lampa_mode and switch_var.get() != "on") or (not config.lampa_mode and switch_var.get() != "off"):
        update_switch_from_lampa_mode()
    if (config.ledy_mode and switch_var_two.get() !="on") or (not config.ledy_mode and switch_var_two.get() != "off"):
        update_switch_from_ledy_mode()
    if (config.gniazdo2_mode and gniazdo2_switch_var.get() != "on") or (not config.gniazdo2_mode and gniazdo2_switch_var.get() != "off"):
        update_gniazdo2()
    app.after(500, periodic_check)


periodic_check()
threading.Thread(target=send_loop, daemon=True).start()
threading.Thread(target=receive_loop, daemon=True).start()
#threading.Thread(target=set_led_mode, daemon=True).start()
threading.Thread(target=periodic_check, daemon=True).start()
threading.Thread(target=getStatus.network_checker, daemon=True).start()
#threading.Thread(target=debug, daemon=True).start()
if __name__ == '__main__':
    app.mainloop()
app.mainloop()