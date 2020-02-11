import sqlalchemy_access
from sqlalchemy import create_engine, Table, Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib
from updater_scripts.config import ACCESS_DATABASE_FILE

# database connection
# !!! Mind the path to the database, please use a local copy and do not access via webdav !!!
Base = declarative_base()
connection_string = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=%s; ExtendedAnsiSQL=1;' % ACCESS_DATABASE_FILE
)
connection_url = "access+pyodbc:///?odbc_connect=%s" % urllib.parse.quote_plus(connection_string)
engine = create_engine(connection_url)

Session = sessionmaker(bind=engine)


# define table as an object, you must provide a primary key!
class pictures_fieldwork(Base):
    __table__ = Table("7_Pictures_fieldwork", Base.metadata, Column("Picture_ID", String, primary_key=True),
                      autoload=True, autoload_with=engine)


class pictures_fieldwork_BH(Base):
    __table__ = Table("77_Pictures_fieldwork_BH", Base.metadata, Column("Picture_ID", String, primary_key=True),
                      autoload=True, autoload_with=engine)


class pictures_fieldwork_Locus(Base):
    __table__ = Table("77_Pictures_fieldwork_Locus", Base.metadata, Column("Picture_ID", String, primary_key=True),
                      autoload=True, autoload_with=engine)


class pictures_fieldwork_Nails(Base):
    __table__ = Table("77_Pictures_fieldwork_Nails", Base.metadata, Column("Picture_ID", String, primary_key=True),
                      autoload=True, autoload_with=engine)


class pictures_fieldwork_Structure(Base):
    __table__ = Table("77_Pictures_fieldwork_Structure", Base.metadata, Column("Picture_ID", String, primary_key=True),
                      autoload=True, autoload_with=engine)


class pictures_fieldwork_Locus_Lot(Base):
    __table__ = Table("777_Pictures_fieldwork_Locus_Lot", Base.metadata, Column("Picture_ID", String, primary_key=True),
                      autoload=True, autoload_with=engine)


class BH_pictures(Base):
    __table__ = Table("7777_BH_Pictures", Base.metadata,
                      Column("BH_Number", String, primary_key=True),
                      Column("picture_url", String, primary_key=True),
                      autoload=True, autoload_with=engine)


class BH_drawings(Base):
    __table__ = Table("7777_BH_drawings", Base.metadata,
                      Column("BH_number", String, primary_key=True),
                      Column("Link_to_BH_drawing", String, primary_key=True),
                      autoload=True, autoload_with=engine)


class locus_drawings(Base):
    __table__ = Table("33_Locus_drawings", Base.metadata, Column("Drawing_No", String, primary_key=True),
                      autoload=True, autoload_with=engine)


class drawings_fieldwork(Base):
    __table__ = Table("6_Drawings_fieldwork", Base.metadata, Column("Drawing_No", String, primary_key=True),
                      autoload=True, autoload_with=engine)


class lot(Base):
    __table__ = Table("4_Lot", Base.metadata,
                      Column("Trench", String, primary_key=True),
                      Column("Lot", Integer, primary_key=True),
                      Column("Date", Date, primary_key=True),
                      autoload=True, autoload_with=engine)
