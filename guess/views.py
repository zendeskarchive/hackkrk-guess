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
        'solved': getattr(riddle, 'solved', False),
        'solved_by': getattr(riddle, 'solved_by', 0),
        'attempted_by': getattr(riddle, 'attempted_by', 0),
        'created_at': riddle.created_at.isoformat() + 'Z',
        }

def attempt_view(attempt):
    return {
        'answer': attempt.answer,
        'successful': attempt.successful
    }

def riddles_listing_view(pager, riddles):
    return {
        'total': pager.total,
        'page': pager.page,
        'page_count': pager.page_count,
        'riddles': [riddle_view(r) for r in riddles]
    }

def user_leader_board_view(user):
    return {
        'username': user.username,
        'score': getattr(user, 'score', 0),
    }

def leaderboard_view(pager, users):
    return {
        'total': pager.total,
        'page': pager.page,
        'page_count': pager.page_count,
        'users': [user_leader_board_view(r) for r in users]
    }

