'''
Created 10/2019 Python 3.7 (2.7 has a problem with sqlalchemy-access)

@author: Peter Vos VU IT for Research

Retrieve image and pdf file lists from mounted webdav connection and update the database with urls

Make sure to:
pip install SQLAlchemy
pip install sqlalchemy-access
set the correct paths in updater_scripts/config.py
'''
import updater_scripts.access as access
import updater_scripts.file_list_builder as file_list_builder
import re

def access_link(url):
    return '#%s#' % url

def picture_id_list(file_list):
    id_list = {}
    for f in file_list:
        basename = f
        url = file_list[f][1]
        m = re.match(r'(.*)_(\d{11}).+', basename)
        if m is not None:
            picture_id = m.group(1)
            flickr_id = m.group(2)
            id_list[picture_id] = url
    return id_list


def update_picture_urls(tbl, file_list):
    print('update %s' % tbl.__name__)
    id_list = picture_id_list(file_list)
    session = access.Session()
    rows = session.query(tbl)
    print('%s records in table' % rows.count())
    total_db = 0
    for row in rows.all():
        if row is not None:
            if row.Picture_ID in id_list:
                total_db = total_db + 1
                row.picture_url = access_link(id_list[row.Picture_ID])
    print('%s picture_urls set in db' % (total_db))
    print('commit changes')
    session.commit()
    session.close()


def update_drawing_urls(tbl, file_list):
    print('update %s' % tbl.__name__)
    session = access.Session()
    rows = session.query(tbl)
    print('%s records in table' % rows.count())
    total_db = 0
    id_list={}
    # Drawing_No should be first 2 parts of filename
    for f in file_list:
        url = file_list[f][1]
        a = f.split('_')
        id='%s_%s' % (a[0],a[1])
        id_list[id]=url
    for row in rows.all():
        if row is not None:
            if row.Drawing_No in id_list:
                total_db = total_db + 1
                row.Drawing_url = access_link(id_list[row.Drawing_No])
    print('%s drawing_urls set in db' % (total_db))
    print('commit changes')
    session.commit()
    session.close()


def update_lot_forms(tbl, file_list):
    print('update %s' % tbl.__name__)
    session = access.Session()
    rows = session.query(tbl)
    print('%s records in table' % rows.count())
    total_db = 0
    for row in rows.all():
        if row is not None:
            try:
                id = '%s_%s_%s_lot_form' % (row.Trench, row.Date.year, int(row.Lot))
                if id in file_list:
                    total_db = total_db + 1
                    row.Link_to_scanned_lot_form = access_link(file_list[id][1])
                else:
                    row.Link_to_scanned_lot_form = ''
            except:
                print('error, no Date?')
                print(row.Trench, int(row.Lot), row.Date)
    session.commit()
    print('%s link_to_scanned_lot_forms set in db' % (total_db))
    print('commit changes')
    session.close()


def update_daily_reports(tbl, file_list):
    print('update %s' % tbl.__name__)
    session = access.Session()
    rows = session.query(tbl)
    print('%s records in table' % rows.count())
    total_db = 0
    for row in rows.all():
        if row is not None:
            try:
                id = '%s_%s_%s_%s_daily_report' % (
                    row.Trench, '{:02}'.format(row.Date.day), '{:02}'.format(row.Date.month), row.Date.year)
                if id in file_list:
                    total_db = total_db + 1
                    row.Link_to_daily_report = access_link(file_list[id][1])
                else:
                    row.Link_to_daily_report = ''
            except:
                print('error, no Date?')
                print(row.Trench, int(row.Lot), row.Date)
    session.commit()
    print('%s link_to_daily_reports set in db' % (total_db))
    print('commit changes')
    session.close()


def update_daily_sketches(tbl, file_list):
    print('update %s' % tbl.__name__)
    session = access.Session()
    rows = session.query(tbl)
    print('%s records in table' % rows.count())
    total_db = 0
    for row in rows.all():
        if row is not None:
            try:
                id = '%s_%s_%s_%s_daily_sketch' % (
                    row.Trench, '{:02}'.format(row.Date.day), '{:02}'.format(row.Date.month), row.Date.year)
                if id in file_list:
                    total_db = total_db + 1
                    row.Link_to_scanned_daily_sketch = access_link(file_list[id][1])
                else:
                    row.Link_to_scanned_daily_sketch = ''
            except:
                print('error, no Date?')
                print(row.Trench, int(row.Lot), row.Date)
    session.commit()
    print('%s link_to_daily_sketches set in db' % (total_db))
    print('commit changes')
    session.close()


def update_bh_picture_urls(tbl, file_list):
    print('update %s' % tbl.__name__)
    session = access.Session()
    total_db = 0
    for f in file_list:
        m = re.match(r'^BH(\d+)_.+', f)
        if m:
            url =file_list[f][1]
            bhnum = m.group(1)
            # a BH_Number can have more than one picture, so the combination is unique
            q = session.query(tbl).filter(tbl.BH_Number == bhnum, tbl.picture_url == url)
            if q.count() == 0:  # new record
                bh = tbl(
                    BH_Number=bhnum,
                    picture_url=access_link(url)
                )
                session.add(bh)
            total_db = total_db + 1
    session.commit()
    print('%s picture_urls set in db' % (total_db))
    print('commit changes')
    session.close()

def update_bh_drawing_urls(tbl, file_list):
    print('update %s' % tbl.__name__)
    session = access.Session()
    total_db = 0
    for f in file_list:
        m = re.match(r'^BH(\d+)_.+', f)
        if m:
            url =file_list[f][1]
            bhnum = m.group(1)
            # a BH_Number can have more than one picture, so the combination is unique
            q = session.query(tbl).filter(tbl.BH_number == bhnum, tbl.Link_to_BH_drawing == url)
            if q.count() == 0:  # new record
                bh = tbl(
                    BH_number=bhnum,
                    Link_to_BH_drawing=access_link(url)
                )
                session.add(bh)
            total_db = total_db + 1
    session.commit()
    print('%s drawing_urls set in db' % (total_db))
    print('commit changes')
    session.close()

def update_trench_reports(tbl, file_list):
    print('update %s' % tbl.__name__)
    session = access.Session()
    total_db = 0
    for f in file_list:
        m = re.match(r'^([A-Z].+)_(\d{4})_trench_report', f)
        if m:
            url =file_list[f][1]
            trench = m.group(1)
            year = m.group(2)
            q = session.query(tbl).filter(tbl.Trench == trench, tbl.Trench_Year == year)
            if q.count() == 0:  # new record
                tr = tbl(
                    Trench=trench,
                    Trench_Year=year,
                    Trench_report_URL=access_link(url)
                )
                session.add(tr)
            total_db = total_db + 1
    session.commit()
    print('%s trench_report_urls set in db' % (total_db))
    print('commit changes')
    session.close()

list_rebuild=True
if input("Get new directory listing? (y/n)")=="n":
    list_rebuild=False

# UPDATE 1
file_list = file_list_builder.get_file_list('PLANS', list_rebuild)
print('%s files found in PLANS' % len(file_list))
update_drawing_urls(access.locus_drawings, file_list)
# UPDATE 2
update_drawing_urls(access.drawings_fieldwork, file_list)
print()

# UPDATE 3
file_list = file_list_builder.get_file_list('LOT_FORMS', list_rebuild)
print('%s files found in LOT_FORMS' % len(file_list))
update_lot_forms(access.lot, file_list)
print()

# UPDATE 4
file_list = file_list_builder.get_file_list('DAILY_REPORTS', list_rebuild)
print('%s files found in DAILY_REPORTS' % len(file_list))
update_daily_reports(access.lot, file_list)
print()

# UPDATE 5
file_list = file_list_builder.get_file_list('SKETCHES', list_rebuild)
print('%s files found in SKETCHES' % len(file_list))
update_daily_sketches(access.lot, file_list)
print()

# UPDATE 6
file_list = file_list_builder.get_file_list('PICTURES', list_rebuild)
print('%s files found in PICTURES' % len(file_list))
update_picture_urls(access.pictures_fieldwork, file_list)
update_picture_urls(access.pictures_fieldwork_BH, file_list)
update_picture_urls(access.pictures_fieldwork_Locus, file_list)
update_picture_urls(access.pictures_fieldwork_Nails, file_list)
update_picture_urls(access.pictures_fieldwork_Structure, file_list)
update_picture_urls(access.pictures_fieldwork_Locus_Lot, file_list)
# UPDATE 7
update_bh_picture_urls(access.BH_pictures, file_list)

# UPDATE 8
file_list = file_list_builder.get_file_list('OBJECT_DRAWINGS', list_rebuild)
print('%s files found in OBJECT_DRAWINGS' % len(file_list))
update_bh_drawing_urls(access.BH_drawings, file_list)

# UPDATE 9
file_list = file_list_builder.get_file_list('TRENCH_REPORTS', list_rebuild)
print('%s files found in TRENCH_REPORTS' % len(file_list))
update_trench_reports(access.trench, file_list)