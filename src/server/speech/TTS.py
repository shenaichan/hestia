import os
import azure.cognitiveservices.speech as speechsdk

def synthesize(text):
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv("AZURE_SPEECH_ACCESS_KEY"), region="eastus")
    speech_config.speech_synthesis_voice_name = "en-US-CoraMultilingualNeural"
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))



