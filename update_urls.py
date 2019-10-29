import updater_scripts.access as access
import updater_scripts.file_list_builder as file_list_builder
import re


def picture_id_list(file_list):
    id_list = {}
    for f in file_list:
        basename = f
        url = file_list[f][1]
        m = re.match(r'(.*)_(\d{11}).+', basename)
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
                row.picture_url = id_list[row.Picture_ID][0]
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
    for row in rows.all():
        if row is not None:
            # base file name should be the Drawing_No
            if row.Drawing_No in file_list:
                total_db = total_db + 1
                row.Drawing_url = file_list[row.Drawing_No][1]
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
                    row.Link_to_scanned_lot_form = file_list[id][1]
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
                    row.Link_to_daily_report = file_list[id][1]
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
                    row.Link_to_scanned_daily_sketch = file_list[id][1]
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
            bhnum = m.group(1)
            q = session.query(tbl).filter(tbl.BH_Number == bhnum)
            if q.count() == 0:  # new record
                bh = tbl(
                    BH_Number=bhnum,
                    picture_url=file_list[f][1]
                )
                session.add(bh)
            else:
                bh = q.first()
                bh.picture_url = file_list[f][1]
            total_db = total_db + 1
    session.commit()
    print('%s picture_urls set in db' % (total_db))
    print('commit changes')
    session.close()


# UPDATE 1
file_list = file_list_builder.get_file_list('PLANS')
print('%s files found in PLANS' % len(file_list))
update_drawing_urls(access.locus_drawings, file_list)
# UPDATE 2
update_drawing_urls(access.drawings_fieldwork, file_list)
print()

# UPDATE 3
file_list = file_list_builder.get_file_list('LOT_FORMS')
print('%s files found in LOT_FORMS' % len(file_list))
update_lot_forms(access.lot, file_list)
print()

# UPDATE 4
file_list = file_list_builder.get_file_list('DAILY_REPORTS')
print('%s files found in DAILY_REPORTS' % len(file_list))
update_daily_reports(access.lot, file_list)
print()

# UPDATE 5
file_list = file_list_builder.get_file_list('SKETCHES')
print('%s files found in SKETCHES' % len(file_list))
update_daily_sketches(access.lot, file_list)
print()

# UPDATE 6
file_list = file_list_builder.get_file_list('PICTURES')
print('%s files found in PICTURES' % len(file_list))
update_picture_urls(access.pictures_fieldwork, file_list)
update_picture_urls(access.pictures_fieldwork_BH, file_list)
update_picture_urls(access.pictures_fieldwork_Locus, file_list)
update_picture_urls(access.pictures_fieldwork_Nails, file_list)
update_picture_urls(access.pictures_fieldwork_Structure, file_list)
update_picture_urls(access.pictures_fieldwork_Locus_Lot, file_list)
# UPDATE 7
update_bh_picture_urls(access.BH_pictures, file_list)

