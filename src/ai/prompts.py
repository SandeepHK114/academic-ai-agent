

##Selecting prompt using if-else logic


def select_system_prompt(mode = str) -> str:

    system_prompt = " "

    if mode == "Quiz":
        system_prompt = "Ask questions aiming to test the user about a concept, this may be questions of any format"
    elif mode == "Note-Taker":
        system_prompt = "Utilzing user prompt, summarize main concepts and generate notes that feel almost handwritten"
    elif mode == "DumbDown":
        system_prompt = "Dumb_down user concept like you are explaining to a 8 year old"
    else:
        system_prompt = "You are an educative assistant that yearns to teach users about any concept"

    return system_prompt







    