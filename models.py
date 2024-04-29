import datetime
from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy import SmallInteger, BigInteger, String, JSON, Time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import create_tables

class MatchORM(Base):
    __tablename__ = "Match"
    id: Mapped[int] = mapped_column(BigInteger,primary_key=True)
    players: Mapped[list["MatchPlayerORM"]] = relationship(back_populates="match_",uselist=True, lazy='selectin')
    game_mode: Mapped[int] = mapped_column(SmallInteger)
    lobby_type: Mapped[int] = mapped_column(SmallInteger,nullable=True)
    league_id: Mapped[int] = mapped_column(nullable=True)
    series_id: Mapped[int] = mapped_column(nullable=True)
    series_type: Mapped[int] = mapped_column(SmallInteger,nullable=True)
    start_time: Mapped[int] = mapped_column(BigInteger)
    match_seq_num: Mapped[int] = mapped_column(BigInteger,nullable=True)
    duration: Mapped[datetime.datetime] = mapped_column(Time)
    dire_score: Mapped[int] = mapped_column(SmallInteger)
    dire_team_id: Mapped[int] = mapped_column(nullable=True)
    radiant_score: Mapped[int] = mapped_column(SmallInteger)
    radiant_team_id: Mapped[int] = mapped_column(nullable=True)
    radiant_win: Mapped[bool] = mapped_column()
    patch: Mapped[int] = mapped_column(SmallInteger)
    region: Mapped[int] = mapped_column(SmallInteger,nullable=True)
    replay_url: Mapped[str] = mapped_column(String(256),nullable=True)
    picks_bans = mapped_column(JSON,nullable=True)

class MatchPlayerORM(Base):
    __tablename__ = "Match_player"
    id: Mapped[int] = mapped_column(primary_key=True)
    match_id: Mapped[int] = mapped_column(BigInteger,ForeignKey("Match.id"))
    match_: Mapped["MatchORM"] = relationship(back_populates="players",uselist=False)
    account_id:  Mapped[int | None] = mapped_column(BigInteger,ForeignKey("Profile.account_id"))
    account_: Mapped["ProfileORM"] = relationship(back_populates="played_matches",uselist=False)

    rank_tier: Mapped[int] = mapped_column(SmallInteger,nullable=True)
    isradiant: Mapped[bool] = mapped_column()
    player_slot: Mapped[int] = mapped_column(SmallInteger)
    party_id: Mapped[int] = mapped_column(SmallInteger,nullable=True)
    party_size: Mapped[int] = mapped_column(SmallInteger,nullable=True)
    personaname: Mapped[str] = mapped_column(String(60))
    name: Mapped[str] = mapped_column(String(60),nullable=True)
    hero_id: Mapped[int] = mapped_column(SmallInteger,nullable=True)
    inventory = mapped_column(JSON,nullable=True)
    hero_damage: Mapped[int] = mapped_column(nullable=True)
    hero_healing: Mapped[int] = mapped_column(nullable=True)
    tower_damage: Mapped[int] = mapped_column(nullable=True)
    movement_by_time = mapped_column(JSON,nullable=True)
    mp_kda: Mapped["MatchPlayerKdaORM"] = relationship(back_populates="match_player",uselist=False, lazy='selectin')
    mp_lvlup: Mapped["MatchPlayerLvlUpORM"] = relationship(back_populates="match_player",uselist=False, lazy='selectin')
    mp_networth: Mapped["MatchPlayerNetworthORM"] = relationship(back_populates="match_player",uselist=False, lazy='selectin')
    
class MatchPlayerKdaORM(Base):
    __tablename__ = "Match_player_kda"
    id: Mapped[int] = mapped_column(primary_key=True)
    match_player_id: Mapped[int] = mapped_column(ForeignKey("Match_player.id"))
    match_player: Mapped["MatchPlayerORM"] = relationship(back_populates="mp_kda",uselist=False)

    kills: Mapped[int] = mapped_column(SmallInteger)
    deaths: Mapped[int] = mapped_column(SmallInteger)
    assists: Mapped[int] = mapped_column(SmallInteger)
    last_hits: Mapped[int] = mapped_column(SmallInteger)
    denies: Mapped[int] = mapped_column(SmallInteger)
    kills_by_time = mapped_column(JSON,nullable=True)
    lhts_by_time = mapped_column(JSON,nullable=True)

class MatchPlayerLvlUpORM(Base):
    __tablename__ = "Match_player_lvlup"
    id: Mapped[int] = mapped_column(primary_key=True)
    match_player_id: Mapped[int] = mapped_column(ForeignKey("Match_player.id"))
    match_player: Mapped["MatchPlayerORM"] = relationship(back_populates="mp_lvlup",uselist=False)

    level: Mapped[int] = mapped_column(SmallInteger)
    xp_per_min: Mapped[int] = mapped_column(SmallInteger)
    ability_upgrades_arr = mapped_column(JSON,nullable=True)

class MatchPlayerNetworthORM(Base):
    __tablename__ = "Match_player_networth"
    id: Mapped[int] = mapped_column(primary_key=True)
    match_player_id: Mapped[int] = mapped_column(ForeignKey("Match_player.id"))
    match_player: Mapped["MatchPlayerORM"] = relationship(back_populates="mp_networth",uselist=False)

    net_worth: Mapped[int] = mapped_column()
    gold_per_min: Mapped[int] = mapped_column(SmallInteger)
    networth_by_time = mapped_column(JSON,nullable=True)
    purchase_by_time = mapped_column(JSON,nullable=True)
    additional_units = mapped_column(JSON,nullable=True)

class ProfileORM(Base):
    __tablename__ = "Profile"
    account_id: Mapped[int] = mapped_column(BigInteger,primary_key=True)
    played_matches: Mapped[list["MatchPlayerORM"]] = relationship(back_populates="account_",uselist=True,lazy='selectin')

    personaname: Mapped[str] = mapped_column(String(60), nullable=True)
    prof_name: Mapped[str] = mapped_column(String(60),nullable=True)
    avatar_src: Mapped[str] = mapped_column(String(120), nullable=True)

class TelegramUserORM(Base):
    __tablename__ = "TelegramUser"
    chat_id: Mapped[int] = mapped_column(BigInteger,primary_key=True)
    account_id: Mapped[int | None] = mapped_column(BigInteger,nullable=True)

#create_tables()