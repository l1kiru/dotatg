from json_parser import parse_replay
from database import session_factory
from models import ProfileORM, MatchPlayerORM, MatchPlayerKdaORM
from models import MatchPlayerNetworthORM, MatchPlayerLvlUpORM, MatchORM

match_id = '7151096532'

with session_factory() as session:
    if(session.get(MatchORM,match_id)):
        match_ = session.get(MatchORM,match_id)
        print('Матч:')
        print(match_.__dict__)
        print('Игрок матча:')
        print(match_.players[9].__dict__)