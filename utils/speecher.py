import pyttsx3


class Speecher:
    """
    """

    def __init__(self, language='pt_BR'):
        """
        """

        #
        self.engine = pyttsx3.init()

        #
        for v in self.engine.getProperty('voices'):
            #
            if v.languages[0] == language:
                #
                self.engine.setProperty('voice', v.id)

    def save(self, text, file_path):
        """
        """

        return self.engine.save_to_file(text, file_path)

    def run(self):
        """
        """

        return self.engine.runAndWait()
