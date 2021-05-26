from dotenv import load_dotenv as dotenv
import os
a = """[setting]
cpu=1
h_dpi=160
h_resolution=960x540
isChangeResolution=YES
manual_perform=true
mem=1000
performance_type=1
system_type=7
frames=50
audio_card=false
v_dpi=160
v_resolution=540x960
last_player_width=772
last_player_height=466
last_player_posx=798
last_player_posy=413
computer_resolution_width=2560
computer_resolution_height=1400

[toolbar_setting]
display_toolbar_add_apk=true
display_toolbar_clip_cursor=true
display_toolbar_close_all=true
display_toolbar_double_fingers=true
display_toolbar_full_screen=true
display_toolbar_keyboard_control=true
display_toolbar_live_streaming=false
display_toolbar_multiplayer=true
display_toolbar_mute=false
display_toolbar_reboot=true
display_toolbar_rom_keys=true
display_toolbar_rom_menu=true
display_toolbar_rotate=false
display_toolbar_screen_cap=true
display_toolbar_script_record=true
display_toolbar_settings_usb=true
display_toolbar_shake=false
display_toolbar_share_folder=true
display_toolbar_synchronous_operate=true
display_toolbar_video_record=false
display_toolbar_virtual_position=true
display_toolbar_volumn_down=false
display_toolbar_volumn_up=false


[sync]
sync_dlg_height=360
sync_dlg_width=512
"""
dotenv()
nox0 = os.getenv("nox0")
nox = os.getenv("nox")

def runnox():
    while True:
        arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        try:
            i = (input("Which nox #?"))
            if i == "0":
                with open(nox0, "w") as f:
                    f.write(a)
            elif i == "all":
                for j in range(10):
                    with open(nox+"{}_conf.ini".format(j), "w") as f:
                        f.write(a)
                with open(nox0, "w") as f:
                    f.write(a) 
            elif i == "stop" or i == "exit":
                break
            else:
                with open(nox+"{}_conf.ini".format(i), "w") as f:
                    f.write(a)
        except Exception as e:
            print(repr(e))
            continue
            
if __name__ == "__main__":
    runnox()
