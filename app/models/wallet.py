from dataclasses import dataclass
from app import db
# Esta sería la clase hija de coin
@dataclass(init=False)
class Wallet(db.Model):
    __tablename__ = 'wallets'
    id_wallet = db.Column('id_wallet',db.Integer, primary_key=True, autoincrement= True)
    balance =  db.Column('balance', db.Integer, nullable=False, default=0)
    # Relación many-to-one: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
    # many wallets - one account
    id_owner_account = db.Column('id_account', db.ForeignKey('accounts.id_account'), nullable=False)
    accounts = db.relationship('Account', back_populates='wallets')
    # Relación many-to-one: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
    # many wallets - one coin
    id_wallet_coin = db.Column('id_coin', db.ForeignKey('coins.id_coin'), nullable=False)
    coin = db.relationship('Coin', back_populates='wallet')
