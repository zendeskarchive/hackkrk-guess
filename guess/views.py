def user_view(user):
    return {
        'username': user.username,
        'token': user.token,
        }

def riddle_view(riddle):
    return {
        'id': riddle.id,
        'question': riddle.question,
        'photo_url': riddle.photo_url,
        'author': riddle.author_name,
        }

def attempt_view(attempt):
    return {
        'answer': attempt.answer,
        'successful': attempt.successful
    }

def riddles_listing_view(riddles):
    ret = []
    for riddle in riddles:
        riddle.answered = any(att.successful for att in riddle.attempts)
        ret.append(riddle)
    return ret
