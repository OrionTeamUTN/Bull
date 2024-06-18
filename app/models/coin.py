from dataclasses import dataclass
from app import db

@dataclass
class Coin(db.Model):
    __tablename__ = 'coins'
    id_coin = db.Column('id_coin', db.Integer, primary_key=True, autoincrement= True)
    coin_name = db.Column('coin_name', db.String(50))
    coin_abbreviation = db.Column('coin_abbreviation', db.String(5))
    id_coin_wallet = db.Column('id_coin_wallet', db.ForeignKey('wallets.id_wallet'), nullable=False)
    wallet = db.relationship('Wallet', back_populates='coin' )