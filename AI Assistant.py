import google.genai as ai #Google GenAI Module for response generation
import speech_recognition as sr #Speech Recognition Module for audio input
import pyttsx3 #Pyttsx3 Module for text to speech conversion


API_KEY="your-api-key" #Stores the API Key for Google GenAI in a variable
client=ai.Client(api_key=API_KEY) #Initializes the Google GenAI client with the provided API key
aimodel="gemini-2.5-flash-lite" #Specifies the AI model to be used for generating responses, in this case, "gemini-2.5-flash-lite"

global code #Defines a global variable "code" to control the flow of the chatbot program, initialized to 1 to start the chatbot loop.
code=1

def chatbot(): #Defines a function named "chatbot" that contains the main logic for the AI assistant
    global code #The function will use the global variable "code" to control the flow of the program
    
    engine = pyttsx3.init() #Initializes the pyttsx3 engine for text-to-speech conversion
    engine.setProperty('rate',140) #Sets the speech rate of the pyttsx3 engine to 140 words per minute for a more natural speaking pace

    r = sr.Recognizer() #Initializes the speech recognizer from the speech_recognition module to capture and process audio input from the user
    with sr.Microphone() as source: #Uses the default microphone as the audio source for capturing user input
        print("Listening...") 
        audio=r.listen(source) #Listens for audio input from the user through the microphone and stores it in the variable "audio"

    try:
        text=r.recognize_google(audio) #Converts the audio input into text using Google's speech recognition service
    except Exception as e: #Catches any exceptions that occur during the speech recognition process and stores the error message in the variable "e"
        print("Error: ",e)
        #Exits the program
        code=0
        return
    
    #Generates a response from the AI model using the captured text input, appending "Answer in short." to prompt the model for a concise response. The generated response is stored in the variable "response".
    response=client.models.generate_content(model=aimodel,contents=text+". Answer in short.")
    engine.say(response.text) #Uses the pyttsx3 engine to convert the generated response text into speech and queues it for playback
    engine.runAndWait() #Runs the speech synthesis and waits for it to complete
    
    #Checks if the generated response contains the words "bye" or "exit" to determine if the user wants to end the conversation. If either word is found in the response, it sets the "code" variable to 0 to exit the chatbot loop.
    word_to_quit="bye"
    word_to_quit2="exit"
    if word_to_quit in response.text or word_to_quit2 in text:
        code=0

while code==1: #Starts a loop that continues to run as long as the "code" variable is equal to 1, allowing the chatbot to keep listening for user input and generating responses until the user decides to exit by saying "bye" or "exit".
    chatbot()
