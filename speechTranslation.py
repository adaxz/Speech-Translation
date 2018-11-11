import speech_recognition as sr
# Imports the Google Cloud client library
from google.cloud import translate

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()


    for i in range(PROMPT_LIMIT):
        print('Speak!'.format(i + 1))
        response = recognize_speech_from_mic(recognizer, microphone)
        if response["transcription"]:
            break
        if not response["success"]:
            break
        print("I didn't catch that. What did you say?\n")
    # if there was an error, stop the game
    if response["error"]:
        print("ERROR: {}".format(response["error"]))
        # break

    print("You said: {}".format(response["transcription"]))

    # Instantiates a client
    translate_client = translate.Client()

    # The target language
    target = 'ja'

    # Translates some text into Russian
    translation = translate_client.translate(
        response["transcription"],
        target_language=target)

    print(u'Translation: {}'.format(translation['translatedText']))
