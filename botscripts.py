def findMatchId(message_text):
    answer = 'Вы не указали id матча.'
    for word in message_text:
        if word.isdigit():
            answer = word
    return answer