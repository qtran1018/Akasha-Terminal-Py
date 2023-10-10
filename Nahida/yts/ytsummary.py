from youtube_transcript_api import YouTubeTranscriptApi

def getTranscription(url):
    #Youtube URL input.
    videoURL = url

    transcript = ""

    #Checks input URL for which version of the YT URL is used, or if neither.
    if "youtube.com/watch?v=" in videoURL:
        posStart = videoURL.rfind('?v=') + 3
        posEnd = posStart + 11
        subURL = videoURL[posStart:posEnd]
    elif "youtu.be/" in videoURL:
        posStart = videoURL.rfind('be/') + 3
        posEnd = posStart + 11
        subURL = videoURL[posStart:posEnd]
    else:
        print("Please use a valid youtube video link.")
        exit()
        
    try:
        # Gets video transcript from input URL.
        srt = YouTubeTranscriptApi.get_transcript(subURL) 

        # iterating through each element of list srt
        for i in srt:
            # writing each element of srt on a new line, if the key is 'text'
            transcript = transcript + str(i['text'])
    except Exception as e:
        transcript = "Send this message back to me:" + str(e)
        print("Error occurred.", e)
    transcript.replace("[Music]","")
    return transcript