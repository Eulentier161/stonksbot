from sqlalchemy.dialects import postgresql
from sqlalchemy import Column, engine, ForeignKey, Text, BigInteger
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
import yaml

with open('config.yaml', 'r') as f:
    _database = yaml.safe_load(f)['database']
DATABASE_USERNAME = _database['username']
DATABASE_PASSWORD = _database['password']
DATABASE_NAME =     _database['name']
DATABASE_ADDRESS =  _database['address']
DATABASE_PORT =     _database['port']
VERBOSE_LOG =       False

engine = engine.create_engine(f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_ADDRESS}:{DATABASE_PORT}/{DATABASE_NAME}', echo=VERBOSE_LOG)


class GuildTable(Base):
    __tablename__ = "guild"
    guild_id = Column(BigInteger, primary_key=True)
    channels = relationship('ChannelTable', backref='guild')
    
    def __repr__(self) -> str:
        return f'{self.guild_id}'

class ChannelTable(Base):
    __tablename__ = "channel"
    channel_id = Column(BigInteger, primary_key=True)
    coin = Column(Text, nullable=False)
    guild_id = Column(BigInteger, ForeignKey(GuildTable.guild_id))
    
    def __repr__(self) -> str:
        return f'{self.channel_id}, {self.coin}, {self.guild_id}'


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
with Session() as session:
    session.commit()
    
def create_or_update_channel(guild_id: int, channel_id: int, coin: str):
    '''create or update a channel to send infos to'''
    with Session() as session:
        session.execute(postgresql.insert(GuildTable).values({"guild_id": guild_id}).on_conflict_do_nothing())
        session.commit()
        content = {"channel_id": channel_id, "coin": coin, "guild_id": guild_id}
        session.execute(postgresql.insert(ChannelTable).values(content).on_conflict_do_update(index_elements=['channel_id'], set_=content))
        session.commit()
        
def delete_channel(channel_id: int):
    '''delete a channel from the db'''
    with Session() as session:
        session.delete(session.query(ChannelTable).get(channel_id))
        session.commit()
        
def get_all_channels() -> list:
    with Session() as session:
        return [channel.__dict__ for channel in session.query(ChannelTable).all()]
    
def get_all_guild_channels(guild_id: int) -> list:
    with Session() as session:
        return [channel.__dict__ for channel in session.query(ChannelTable).filter(ChannelTable.guild_id==guild_id)]
    
def get_channel(channel_id: int) -> dict:
    with Session() as session:
        return session.query(ChannelTable).get(channel_id).__dict__