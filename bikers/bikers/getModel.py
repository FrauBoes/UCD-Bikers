# This was code to use SQL alchemy for database connecttion.
# We dicided not to use this due to implementation challenges with the given time restraints



# from flask import Flask, render_template, request, jsonify, g
# from flask_sqlalchemy import SQLAlchemy
# import pymysql
# 
# 
# def connect_to_database():
#     engine = create_engine('mysql+pymysql://aws137482dd:bikerz123@bikedata.c33719womxye.us-east-2.rds.amazonaws.com:3306/BikeData', connect_args={"encoding": "utf8"}, echo=True)
#     return engine
#                                                                                                                                                      
# 
# def get_db():
#     engine = getattr(g, 'engine', None)
#     if engine is None:
#         engine = g.engine = connect_to_database()
#     return engine
#  
#  
# def get_station_occupancy(w, n):
#     engine = get_db()
#     sql = "SELECT TIME, NUMBER_OF_BIKES, NUMBER_OF_STANDS FROM BIKEDATA WHERE DAYOFWEEK(FROM_UNIXTIME(TIME/1000)) = {} AND STATION_NUMBER = {} ORDER BY TIME ASC".format(w,n)
#     rows = engine.execute(sql).fetchall()
#     print('#found {} stations', len(rows))
#     return jsonify(stations=[dict(row.items()) for row in rows])
#      
#      
# # data = pd.read_sql_table('data', conn)
