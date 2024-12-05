import streamlit as st
import pyttsx3
import io
import os

def text_to_speech(text):
    """
    Convert input text to speech using pyttsx3 library.
    
    Args:
        text (str): Input text to convert to speech.
    
    Returns:
        bytes: Audio file in bytes.
    """
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    
    # Create an in-memory bytes buffer
    audio_buffer = io.BytesIO()
    
    # Save audio to a temporary file
    engine.save_to_file(text, "temp_audio.wav")
    engine.runAndWait()
    
    # Read the temporary audio file into the buffer
    with open("temp_audio.wav", "rb") as audio_file:
        audio_buffer.write(audio_file.read())
    
    # Remove the temporary file
    os.remove("temp_audio.wav")
    
    # Reset buffer position
    audio_buffer.seek(0)
    
    return audio_buffer.getvalue()

def main():
    """
    Main Streamlit application for text-to-speech conversion.
    """
    # Set page title and icon
    st.set_page_config(page_title="Text-to-Speech Converter", page_icon="🔊")
    
    # Title and description
    st.title("Text-to-Speech Converter 🎙️")
    st.write("Upload a `.txt` file or paste text into the application to convert it to speech.")
    
    # Option to upload a file or paste text
    text_source = st.radio("Choose text input method:", options=["Upload .txt File", "Paste Text"])
    
    user_text = ""
    if text_source == "Upload .txt File":
        uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])
        if uploaded_file is not None:
            # Read content from the uploaded .txt file
            try:
                user_text = uploaded_file.read().decode("utf-8")
                st.success("File successfully uploaded.")
                st.text_area("Uploaded Text Preview:", user_text, height=200, disabled=True)
            except Exception as e:
                st.error(f"Error reading file: {e}")
    elif text_source == "Paste Text":
        user_text = st.text_area("Enter text here:", placeholder="Type or paste your text here...", height=200)
    
    # Conversion button
    if st.button("Convert Text to Speech"):
        if user_text.strip():
            try:
                # Convert text to speech
                audio_bytes = text_to_speech(user_text)
                
                # Play audio
                st.audio(audio_bytes, format="audio/wav")
                
                # Download button
                st.download_button(
                    label="Download Audio File",
                    data=audio_bytes,
                    file_name="text_to_speech_output.wav",
                    mime="audio/wav"
                )
                
                st.success("Text successfully converted to speech!")
            
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please provide some text either by uploading a .txt file or pasting it.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
