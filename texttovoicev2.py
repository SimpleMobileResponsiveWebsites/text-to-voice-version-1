from gtts import gTTS
import streamlit as st
import io

def text_to_speech_gtts(text):
    """
    Convert input text to speech using gTTS (Google Text-to-Speech).
    """
    tts = gTTS(text)
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer.getvalue()

def main():
    st.title("Text-to-Speech Converter with gTTS 🎙️")
    user_text = st.text_area("Enter text here:", placeholder="Type or paste your text here...")
    
    if st.button("Convert Text to Speech"):
        if user_text.strip():
            audio_bytes = text_to_speech_gtts(user_text)
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                label="Download Audio File",
                data=audio_bytes,
                file_name="text_to_speech_output.mp3",
                mime="audio/mp3"
            )
        else:
            st.warning("Please enter some text before converting.")

if __name__ == "__main__":
    main()
