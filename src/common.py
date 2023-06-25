from playsound import playsound

def playy():
    """This method will be used to play the beep sound.
        
        :param: None.

        :returns: Nothing.
    """     
    playsound('../audio/beep.mp3', block=False)