from dataclasses import dataclass
from app import db

@dataclass
class Coin(db.Model):
    __tablename__ = 'coins'
    id_coin = db.Column('id_coin', db.Integer, primary_key=True, autoincrement= True)
    coin_name = db.Column('coin_name', db.String(50))
    coin_abbreviation = db.Column('coin_name', db.String(5))
    coin = db.relationship('Wallet',  uselist=False, back_populates='coin' )    

    