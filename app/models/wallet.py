from dataclasses import dataclass
from app import db
@dataclass
class Wallet( db.Model ):
    __tablename__ = 'wallets'
    id_wallet = db.Column('id_wallet',db.Integer, primary_key=True, autoincrement= True)
    balance =  db.Column('balance', db.Integer, nullable=False, default=0)
    id_owner_account = db.Column('id_account', db.ForeignKey('Account.id_account'), nullable=False, ondelete="restrict")
    account = db.relationship('Account', uselist=False, back_populates='wallet')
    id_wallet_coin = db.Column('id_wallet_coin', db.ForeingKey('Coin.id_coin'), nullable=False, ondelete="restrict")
    coin = db.relationship('Coin', uselist=False, back_populates='wallet')
    