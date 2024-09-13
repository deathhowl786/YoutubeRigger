import customtkinter as ctk
from pytube import YouTube
from PIL import Image 
import os
import urllib.request
from textwrap import wrap

# function to remove special characters from a url and make a unique name for each video.
def urlCleaner(url):
    temp = ""
    chars = [";", ",", "?", ":", "@", "&", "=", "+", "$", "-", "_", ".", "!", "~", "*", "'", "#"]
    for i in url.split("/")[-1]:
        if(i not in chars):
            temp += i
    return temp

# function which runs the App
def runApp():

    default_res = "1080p"
    download_folder = "Downloads"

    # reset function to bring back all widgets to default settings
    def reset():
        urlEntry.delete(0, ctk.END)  # deletes all text
        res_dropdown.set(default_res)

        # removes the widget from the interface [unpacks]
        statusLabel.pack_forget()
        progressLabel.pack_forget()
        progressBar.set(0)
        progressBar.pack_forget()
        viewlabel.pack_forget()

    # function to keep track of the downloading
    def progress_track(stream, chunk, bytes_remaining):

        # Necessary Calculations
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        download_percentage = bytes_downloaded / total_size

        # Making the required Widgets [Progress Label and Bar] Visible
        progressLabel.pack(pady=(12, 0), padx=10)
        progressBar.pack(pady=(0, 12), padx=10)
        # Constantly updating Progress Label
        progressLabel.configure(text=str(int(download_percentage * 100)) + "%")
        progressBar.set(float(download_percentage))
        progressLabel.update()



    # Function which view the details of the Video
    def view_video():
        viewlabel.update()
        viewlabel.pack(pady=(12, 0), padx=10)
        statusLabel.update()
        statusLabel.pack(pady=12, padx=10)

        try:
            url = urlEntry.get()
            yt = YouTube(url, on_progress_callback=progress_track)
            
            urllib.request.urlretrieve( 
            yt.thumbnail_url, os.path.join("assets", "thumbnail.png"))
            viewImage = ctk.CTkImage(
            light_image=Image.open(os.path.join("assets", "thumbnail.png")) , dark_image=Image.open(os.path.join("assets", "thumbnail.png")) , size=(350, 200)
            )
            viewlabel.configure(image = viewImage)

            statusLabel.configure(
                    text= f"{'\n'.join(wrap(yt.title, width=50))}",
                    text_color="black",
                    fg_color="red",
                    width=195,
                    corner_radius=6
                )
        except Exception as e:
            print(e)
            statusLabel.configure(
                    text= f"Please Provide Valid URL.",
                    text_color="black",
                    fg_color="red",
                    width=195,
                    corner_radius=6
                )



    # Function which downloads the Video
    def download_video():

        view_video()

        # storing user input url and resolution
        url = urlEntry.get()
        res = res_dropdown.get()
        # File path
        file_path = os.path.join(download_folder, f"[{res}]{urlCleaner(url)}.mp4")


        # Updating the Status Label
        statusLabel.update()
        statusLabel.pack(pady=12, padx=10)

        if(os.path.exists(file_path)):
            
            statusLabel.configure(
                text= f"Video Already Exists :\n{file_path.split("\\")[-1]}",
                text_color="black",
                fg_color="red",
                width=195,
                corner_radius=6
            )
            return None

        # If Video Downloads Successfully
        try:

            # Downloading... Status Label
            statusLabel.configure(
                text="Downloading Video ...",
                text_color="black",
                fg_color="yellow",
                width=195,
                corner_radius=6
            )

            # Creating Object of Youtube with the provided url and checking if resolution available
            yt = YouTube(url, on_progress_callback=progress_track)
            video_stream = yt.streams.filter(res = res, only_video = True).first()
            audio_stream = yt.streams.filter(only_audio= True).last()

            path = os.path.join(download_folder)  # selecting path of download

            # Downloading video to that path
            video_stream.download(output_path=path, filename="VIDEO.mp4")
            audio_stream.download(output_path=path, filename="AUDIO.mp4")
            video_path = os.path.join(download_folder, "VIDEO.mp4")
            audio_path = os.path.join(download_folder, "AUDIO.mp4")


            # Compiling... Staus Label
            statusLabel.configure(
                text="Compiling...",
                text_color="black",
                fg_color="orange",
                width=195,
                corner_radius=6
            )
            statusLabel.update()

            # Merging the video and audio
            command = f"ffmpeg -i {video_path} -i {audio_path} -c:v copy -c:a aac -map 0:v -map 1:a {file_path}"
            os.system(command)
            os.remove(video_path)
            os.remove(audio_path)


            # Download Complete Status Label
            statusLabel.configure(
                text="Download Complete",
                text_color="black",
                fg_color="light green",
                width=195,
                corner_radius=6
            )

        # if Video Fails to Download
        except Exception as e:
            viewlabel.pack_forget()
            # Error Status label
            statusLabel.configure(
                text=f"Couldn't Download Video\n\nProvide a Valid URL\nOR\nTry With a different Resolution\n[Only 30fps Supported]\n\nError : {e}",
                text_color="white",
                fg_color="red",
                width=100,
            )




    # Creating Object ctk [root window]
    root = ctk.CTk()

    # presetting font and image to be used in the .....................
    my_font = ctk.CTkFont(family="Courier New", size=25, weight="bold")
    thumbnail_img = Image.open(os.path.join("assets", "yt_logo.png"))


    # setting icon, geometry, mode and title of app
    root.iconbitmap(os.path.join("assets", "yt_logoo.ico"))
    root.geometry("1080x840")
    root._set_appearance_mode("dark")
    root.title(" Youtube Rigger")


    # setting a default theme by using a custom theme made by themeMaker.py
    ctk.set_default_color_theme(os.path.join("assets", "theme.json"))


    # Creating frame and packing it
    root_frame = ctk.CTkFrame(master=root)
    root_frame.pack(fill=ctk.BOTH, expand=True, pady=12, padx=10)


    # <<===== Creating Widgets =====>>

    # ctk image which is further used in as a label
    thumbnailImage = ctk.CTkImage(
        light_image=thumbnail_img, dark_image=thumbnail_img, size=(200, 150)
    )
    thumbnaillabel = ctk.CTkLabel(master=root_frame, text="", image=thumbnailImage)
    thumbnaillabel.pack(pady=(12, 0), padx=10)


    # ctk a label and entry to take user input
    urlLabel = ctk.CTkLabel(master=root_frame, text="Enter URL Here", font=my_font)
    urlLabel.pack(pady=(12, 0), padx=10)
    urlEntry = ctk.CTkEntry(
        master=root_frame, placeholder_text="URL", width=300, font=my_font
    )
    urlEntry.pack(pady=12, padx=10)


    # ctk download button which navigates view_video() function
    view_btn = ctk.CTkButton(
        master=root_frame, text="VIEW", font=my_font, command=view_video
    )
    view_btn.pack(pady=12, padx=10)


    # ctk download button which navigates download_video() function
    download_btn = ctk.CTkButton(
        master=root_frame, text="DOWNLOAD", font=my_font, command=download_video
    )
    download_btn.pack(pady=12, padx=10)


    # ctk dropdwon to take user input
    resolutions = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]  # preset resloutions
    
    res_dropdown = ctk.CTkOptionMenu(
        master=root_frame, values=resolutions, font=my_font
    )
    res_dropdown.pack(pady=12, padx=10)
    res_dropdown.set(default_res)


    # ctk progress label and bar which tracks the download progress
    progressLabel = ctk.CTkLabel(master=root_frame, font=my_font)
    progressBar = ctk.CTkProgressBar(master=root_frame, width=300)
    progressBar.set(0)  # default values
    # ctk status label to indicate message
    statusLabel = ctk.CTkLabel(master=root_frame, text="...", font=my_font)


    # ctk button which navigates to reset() function used to bring back default settings
    reset_btn = ctk.CTkButton(
        master=root_frame, text="RESET", font=my_font, command=reset
    )
    reset_btn.pack(pady=12, padx=10)


    viewlabel = ctk.CTkLabel(master=root_frame, text="", image=None)

    # running the app
    root.mainloop()



# main function
def main() -> None:
    runApp()



# runs the main function
if __name__ == "__main__":
    main()

