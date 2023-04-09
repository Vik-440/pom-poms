from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.clients.models import DB_client
from app.products.models import DB_product
from app.orders.models import DB_orders
from app import engine


def validate_id_order(id_order: int):
    """Validator for ID order number"""
    with Session(engine) as session:
        stmt = (
            select(DB_orders.id_order)
            .where(DB_orders.id_order == id_order))
        if not session.execute(stmt).first():
            return {'id_order': f'ID order {id_order} is not exist'}
    return



def validate_create_order(data: dict):
    """Validator for create order"""
    qty_product_in_order = None
    # formats_date = ['%Y-%m-%d', '%Y-%-m-%-d']
    date_today = datetime.today().strftime('%Y-%m-%d')
    with Session(engine) as session:

        if not 'date_create' in data:
            return {"date_create": 'miss in data'}
        if not isinstance(data['date_create'], str):
            return {'date_create': 'is not str type'}
        date_str = data['date_create']
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return {"date_create": 'is not in format like: yyyy-mm-dd'}
        if date_str > date_today:
            return {"date_create": 'date future -> misstake'}
        else:
            data['date_create'] = date_str

        if not 'date_plane_send' in data:
            return {"date_plane_send": 'miss in data'}
        if not isinstance(data['date_plane_send'], str):
            return {'date_plane_send': 'is not str type'}
        date_str = data['date_plane_send']
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return {"date_plane_send": 'is not in format like: yyyy-mm-dd'}
        data['date_plane_send'] = date_str
        
        if not 'id_client' in data:
            return {'id_client': 'miss in data'}
        if not isinstance(data['id_client'], int):
            return {'id_client': 'is not int type'}
        stmt = (
            select(DB_client.id_client)
            .where(DB_client.id_client == data['id_client']))
        if not session.execute(stmt).first():
            return {'id_client': 'ID is not real'}

        if not 'id_recipient' in data:
            return {'id_recipient': 'miss in data'}
        if not isinstance(data['id_recipient'], int):
            return {'id_recipient': 'is not int type'}
        stmt = (
            select(DB_client.id_client)
            .where(DB_client.id_client == data['id_recipient']))
        if not session.execute(stmt).first():
            return {'id_recipient': 'ID is not real'}

        if not 'status_order' in data:
            return {'status_order': 'miss in data'}
        if not isinstance(data['status_order'], bool):
            return {'status_order': 'is not bool type'}

        if not 'sum_payment' in data:
            return {'sum_payment': 'miss in data'}
        if not isinstance(data['sum_payment'], int):
            return {'sum_payment': 'is not int type'}

        if not 'discount' in data:
            return {'discount': 'miss in data'}
        if not isinstance(data['discount'], int):
            return {'discount': 'is not int type'}

        if not 'comment' in data:
            return {"comment":  "miss in data"}
        if not isinstance(data['comment'], str) and not data['comment'] is None:
            return {'comment': 'is not str or None type'}
        
        if not 'id_models' in data:
            return {'id_models': 'miss in data'}
        if not isinstance(data['id_models'], list):
            return {'id_models': 'is not list type'}
        qty_product_in_order = len(data['id_models'])
        if qty_product_in_order == 0:
            return {'id_models': 'is empty'}
        for id_product in data['id_models']:
            if not isinstance(id_product, int):
                return {'id_models': f'{id_product} is not int type'}
            stmt = (
                select(DB_product.id_product)
                .where(DB_product.id_product == id_product))
            if not session.execute(stmt).first():
                return {'id_models': f'ID product {id_product} is not real'}

        if not 'qty_pars' in data:
            return {'qty_pars': 'miss in data'}
        if not isinstance(data['qty_pars'], list):
            return {'qty_pars': 'is not list type'}
        if qty_product_in_order != len(data['qty_pars']):
            return {'qty_pars': 'qty positions in qty_pars is not eiqual qty in id_models'}
        for qty_pars_item in data['qty_pars']:
            if not isinstance(qty_pars_item, int):
                return {'qty_pars': f'{qty_pars_item} in qty_pars is not int type'}

        if not 'phase_1' in data:
            return {'phase_1': 'miss in data'}
        if not isinstance(data['phase_1'], list):
            return {'phase_1': 'is not list type'}
        if qty_product_in_order != len(data['phase_1']):
            return {'phase_1': 'qty positions in phase_1 is not eiqual qty in id_models'}
        for index, phase_1_item in enumerate(data['phase_1']):
            if not isinstance(phase_1_item, int):
                return {'phase_1': f'{phase_1_item} in phase_1 is not int type'}
            if data['qty_pars'][index] * 2 < phase_1_item:
                return {'phase_1': f'{phase_1_item} in phase_1 is bigger then it is possible (qty_pars * 2)'}

        if not 'phase_2' in data:
            return {'phase_2': 'miss in data'}
        if not isinstance(data['phase_2'], list):
            return {'phase_2': 'is not list type'}
        if qty_product_in_order != len(data['phase_2']):
            return {'phase_2': 'qty positions in phase_2 is not eiqual qty in id_models'}
        for index, phase_2_item in enumerate(data['phase_2']):
            if not isinstance(phase_2_item, int):
                return {'phase_2': f'{phase_2_item} in phase_2 is not int type'}
            if data['qty_pars'][index] * 2 < phase_2_item:
                return {'phase_2': f'{phase_2_item} in phase_2 is bigger then it is possible (qty_pars * 2)'}

        if not 'phase_3' in data:
            return {'phase_3': 'miss in data'}
        if not isinstance(data['phase_3'], list):
            return {'phase_3': 'is not list type'}
        if qty_product_in_order != len(data['phase_3']):
            return {'phase_3': 'qty positions in phase_3 is not eiqual qty in id_models'}
        for index, phase_3_item in enumerate(data['phase_3']):
            if not isinstance(phase_3_item, int):
                return {'phase_3': f'{phase_3_item} in phase_3 is not int type'}
            if data['qty_pars'][index] < phase_3_item:
                return {'phase_3': f'{phase_3_item} in phase_3 is bigger then it is possible (qty_pars)'}

        if not 'price_model_sell' in data:
            return {'price_model_sell': 'miss in data'}
        if not isinstance(data['price_model_sell'], list):
            return {'price_model_sell': 'is not list type'}
        if qty_product_in_order != len(data['price_model_sell']):
            return {'price_model_sell': 'qty positions in price_model_sell is not eiqual qty in id_models'}
        for price_model_sell_item in data['price_model_sell']:
            if not isinstance(price_model_sell_item, int):
                return {'price_model_sell': f'{price_model_sell_item} in price_model_sell is not int type'}

    return 
