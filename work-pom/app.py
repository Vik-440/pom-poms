from sqlalchemy import create_engine, true 
from flask import Flask,jsonify,request

log_pass_sql = 'postgresql+psycopg2://postgres:123123@localhost/postgres'
engine = create_engine(log_pass_sql)


def get_data_from_table(cond_tmp):
    with engine.connect() as connection:
        result=connection.execute(cond_tmp)
        #print(result.fetchall())
        for row in result:
             print (row) 


id_order = get_data_from_table ('SELECT id_order FROM directory_of_order WHERE fulfilled_order = FALSE')
#data_order = get_data_from_table ('SELECT data_order FROM directory_of_order WHERE fulfilled_order = FALSE')

# print ('Color')
# get_data_from_table('id_color',	'name_color', 'directory_of_color')
# print ('Order')
# get_data_from_table('id_order', 'data_order', 'directory_of_order')
# print ('client')
# get_data_from_table('phone_client',	'second_name_client','directory_of_client')


app =   Flask(__name__)
  
@app.route('/')
def Home():

    info = {'username':'eduCBA', 'account':'Premium', 'validity':'2709 days','baby':'two years'}
    return jsonify(info) # returning a JSON response
  
if __name__=='__main__':
    app.run(debug=True)