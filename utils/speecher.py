import pyttsx3


class Speecher:
    """Wraps pyttsx3 to ease its usage in a text-to-speech pipeline.

    """

    def __init__(self, language='pt_BR'):
        """Initialization method.

        Args:
            language (str): Language identifier.

        """

        # Initializes the engine
        self.engine = pyttsx3.init()

        # Iterates through every voice
        for v in self.engine.getProperty('voices'):
            # If the iterated voice corresponds to the selected one
            if v.languages[0] == language:
                # Applies to the engine
                self.engine.setProperty('voice', v.id)

    def save(self, text, file_path):
        """Saves a text to an .ogg file.

        Args:
            text (str): Text to be interpreted.
            file_path (str): Path to the file that will be saved.

        """

        return self.engine.save_to_file(text, file_path)

    def run(self):
        """Runs a text-to-speech process.

        """

        return self.engine.runAndWait()
