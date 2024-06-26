from app import db
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Swap(db.Model):
    __tablename__ = 'swaps'
    
    id_swap: int = db.Column('id_swap', db.Integer, primary_key=True, autoincrement=True)
    operation_date: datetime = db.Column('operation_date', db.DateTime, nullable=False, default=datetime.utcnow()) # fecha actual por default
    amount_send: int = db.Column('amount_send', db.Integer, nullable=False)
    amount_recv: int = db.Column('amount_recv', db.Integer, nullable=False)
    id_wallet_send: int = db.Column('id_wallet_send', db.Integer, db.ForeignKey('wallets.id_wallet'), nullable=False)
    id_wallet_recv: int = db.Column('id_wallet_recv', db.Integer, db.ForeignKey('wallets.id_wallet'), nullable=False)

    wallet_send = db.relationship('Wallet', uselist=False, back_populates='swap_send', primaryjoin='Swap.id_wallet_send == Wallet.id_wallet')
    wallet_recv = db.relationship('Wallet', uselist=False, back_populates='swap_recv', primaryjoin='Swap.id_wallet_recv == Wallet.id_wallet')
    # Indicamos con que atributos de cada clase se hace la relación, necesario cuando tenemos varias foreign keys que hacen referencia una misma columna de la otra tabla

    # Restricciones
    db.CheckConstraint('amount_send > 0')
    db.CheckConstraint('amount_recv > 0')
    db.CheckConstraint('id_wallet_send != id_wallet_recv')
