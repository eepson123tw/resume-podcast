import gradio as gr
from podcastfy.client import generate_podcast
from markitdown import MarkItDown
from IPython.display import Audio, display
import os

class PodcastMarkdownApp:
    def __init__(self):
        self.markitdown = MarkItDown()

    def embed_audio(audio_file):
        """
        Embeds an audio file in the notebook, making it playable.

        Args:
            audio_file (str): Path to the audio file.
        """
        try:
            display(Audio(audio_file))
            print(f"Audio player embedded for: {audio_file}")
        except Exception as e:
            print(f"Error embedding audio: {str(e)}")
        
    def process_file(self, file):
        """
        Convert the uploaded file to text content
        
        Args:
            file (str): Path to the uploaded file
        
        Returns:
            str: Extracted text content
        """
        try:
            result = self.markitdown.convert(file.name)
            return result.text_content
        except Exception as e:
            return f"Error processing file: {str(e)}"

    def generate_podcast_from_text(self, text):
        """
        Generate a podcast audio file from input text
        
        Args:
            text (str): Input text to convert to audio
        
        Returns:
            str: Path to generated audio file
        """
        custom_config = {
            "word_count": 200,
            "conversation_style": ["casual", "humorous"],
            "podcast_name": "Tech Chuckles",
            "creativity": 0.7
        }

        try:
            if not text:
                return None
            
            # Truncate text if too long
            if len(text) > 500:
                text = text[:500] + "... (truncated for podcast generation)"
            # audio_file = generate_podcast(text=text,tts_model="openai", llm_model_name="gpt-4-turbo",api_key_label="OPENAI_API_KEY")
            audio_file = generate_podcast(text=text,is_local=True,llm_model_name='Meta-Llama-3-8B-Instruct',tts_model="openai",)
            return audio_file
        except Exception as e:
            print(f"Podcast generation error: {str(e)}")
            return None

    def create_interface(self):
        """
        Create Gradio interface for file conversion and podcast generation
        
        Returns:
            gr.Blocks: Gradio interface
        """
        with gr.Blocks(title="MarkItDown Podcast Generator") as demo:
            gr.Markdown("# MarkItDown Podcast Generator")
            gr.Markdown("Convert files to text and generate podcasts from content!")
            
            with gr.Tab("File to Text Converter"):
                file_input = gr.File(
                    type="filepath",
                    label="Upload file",
                    file_types=[
                        ".pdf", ".pptx", ".docx", ".xlsx",
                        ".jpg", ".jpeg", ".png",
                        ".mp3", ".wav",
                        ".html",
                        ".csv", ".json", ".xml", ".txt"
                    ]
                )
                text_output = gr.Textbox(label="Extracted Text")
                convert_btn = gr.Button("Convert File")
                convert_btn.click(
                    fn=self.process_file, 
                    inputs=file_input, 
                    outputs=text_output
                )
            
            with gr.Tab("Text to Podcast"):
                text_input = gr.Textbox(
                    label="Enter text to convert to podcast", 
                    info="Maximum 500 characters recommended"
                )
                audio_output = gr.Audio(label="Generated Podcast")
                generate_btn = gr.Button("Generate Podcast")
                generate_btn.click(
                    fn=self.generate_podcast_from_text, 
                    inputs=text_input, 
                    outputs=audio_output
                )
            
            # Example inputs to help users understand the app
            gr.Examples(
                examples=[
                    ["Sample text about AI", "The rapid advancement of artificial intelligence is transforming industries worldwide."],
                    ["Tech innovation", "Machine learning algorithms are revolutionizing how we process and understand data."]
                ],
                inputs=[text_input],
                outputs=[audio_output],
                fn=self.generate_podcast_from_text,
                cache_examples=False
            )

            # Add a note about podcast generation
            gr.Markdown("""
            ### ⚠️ Podcast Generation Note
            - Podcast generation requires Google Cloud credentials
            - If you're seeing errors, you'll need to set up Google Cloud authentication
            - Text is limited to approximately 500 characters
            - Service availability may vary
            """)

        return demo

    def launch(self, share=True):
        """
        Launch the Gradio interface
        
        Args:
            share (bool): Whether to create a public shareable link
        """
        app = self.create_interface()
        app.launch(share=share)

# Create and launch the app
if __name__ == "__main__":
    podcast_app = PodcastMarkdownApp()
    podcast_app.launch()
