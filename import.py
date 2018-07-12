import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f=open("zips.csv")
    reader= csv.reader(f)
    for Zipcode,City,State,Lat,Long,Population in reader:
        db.execute("INSERT INTO city (zipcode,city,state,latitude,longitude,population) VALUES (:zipcode, :city, :state, :latitude, :longitude, :population)",
        {"zipcode": str(Zipcode),"city": City,"state": State,"latitude": Lat,"longitude": Long,"population": Population})
        print(f" Added city information from {Zipcode} to {Population} to the table")
    db.commit()

if __name__=="__main__":
    main()

