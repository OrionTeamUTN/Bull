from dataclasses import dataclass
from app import db
@dataclass(init=False)
class Wallet(db.Model):
    __tablename__ = 'wallets'
    id_wallet = db.Column('id_wallet',db.Integer, primary_key=True, autoincrement= True)
    balance =  db.Column('balance', db.Integer, nullable=False, default=0)
    id_owner_account = db.Column('id_account', db.ForeignKey('accounts.id_account'), nullable=False)
    accounts = db.relationship('Account', uselist=False, back_populates='wallets')
    id_wallet_coin = db.Column('id_coin', db.ForeignKey('coins.id_coin'), nullable=False) #Buscar como agregarle en ondelete restrict -- no fuciona con ondelete='restrict'
    #coin = db.relationship('Coin', uselist=False, back_populates='wallet')
    def add_account(self, account):
        if account not in self.accounts:
            self.accounts.append(account)
    
    def remove_user(self, account):
        if account in self.accounts:
            self.accounts.remove(account)
            
    def add_coin(self, coin):
        if coin not in self.coin:
            self.coin.append(coin)
    
    def remove_user(self, coin):
        if coin in self.coin:
            self.coin.remove(coin)
    
    