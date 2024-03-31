import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from pytube import YouTube
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

class YouTubeToMP3App(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Input field for the YouTube link
        self.url_input = TextInput(text='Enter any yt link to turn into an mp3 file', multiline=False)
        layout.add_widget(self.url_input)

        # Button to trigger the download
        download_button = Button(text='Download as MP3')
        download_button.bind(on_press=self.download_audio)
        layout.add_widget(download_button)

        return layout

    def download_audio(self, instance):
        link = self.url_input.text
        output_path = os.path.join(os.path.expanduser('~'), 'Download')
        os.makedirs(output_path, exist_ok=True)
        try:
            self.download_youtube_audio(link, output_path)
        except Exception as e:
            print(f"Error downloading audio: {e}")

    def download_youtube_audio(self, link, output_path):
        video = YouTube(link)
        stream = video.streams.filter(only_audio=True).first()
        new_name = os.path.splitext(stream.title)
        stream.download(output_path)
        os.rename(os.path.join(output_path, stream.default_filename), os.path.join(output_path, new_name[0] + '.mp3'))
        self.show_popup()

    def show_popup(self):
        popup_content = BoxLayout(orientation='vertical')
        popup_content.add_widget(Button(text='Ok', on_press=self.dismiss_popup))

        self.popupWindow = Popup(title="Download Complete", content=popup_content, size_hint=(None, None), size=(400, 200))
        self.popupWindow.open()

    def dismiss_popup(self, instance):
        self.popupWindow.dismiss()

if __name__ == '__main__':
    YouTubeToMP3App().run()
