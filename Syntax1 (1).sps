* Encoding: UTF-8.
GET DATA
/TYPE=XLS
/FILE='C:\dataAnalysis\panel\vote2022\demogs.xls'
/SHEET=name 'demogs'
/CELLRANGE=full
/READNAMES=on
/ASSUMEDSTRWIDTH=32767.
DATASET NAME DataSet1 WINDOW=FRONT.

compute age = 2024-byear.
VARIABLE LABELS age 'גיל'.
VARIABLE LABELS byear 'שנת לידה'.
recode age (15 thru 24=1)(25 thru 34=2)(35 thru 44=3)(45 thru 54=4)(55 thru 64=5)(65 thru high=6) into agegr.

VARIABLE LABELS agegr 'קבוצות גיל'.
VALUE LABELS agegr
1 '15-24'
2 '25-34'
3 '35-44'
4 '45-54'
5 '55-64'
6 '65+'.


VARIABLE LABELS alyayear 'שנת עלייה'.

VARIABLE LABELS sex 'מין'.
VALUE LABELS sex
1 'זכר'
2 'נקבה'.

VARIABLE LABELS edu 'השכלה'.
VALUE LABELS edu
1 'עד 8 שנל'
2 '9-10 שנל'
3 '11-12 שנל'
4 'תלמיד תיכון'
5 'בוגר תיכון'
6 'במהלך לימודים על תיכוניים לא אקדמיים'
7 'בוגר לימודים על תיכוניים לא אקדמיים'
8 'במהלך לימודי תואר ראשון'
9 'בוגר תואר ראשון'
10 'במהלך לימודי תואר שני'
11 'בוגר תואר שני'
12 'במהלך עבודת דוקטורט'
13 'בעל תואר דוקטור'.

VARIABLE LABELS rel 'קהילה דתית'.
VALUE LABELS rel
1 'יהודי'
2 'נוצרי'
3 'מוסלמי'
4 'דרוזי'
5 'אחר'
6 'חסר דת'.

VARIABLE LABELS relid 'הזדהות עם הדת'.
VALUE LABELS relid
1 'חילוני'
2 'מסורתי'
3 'דתי'
4 'חרדי'.

VARIABLE LABELS ses 'הכנסה'.
VALUE LABELS ses
0 'אין בכלל הכנסה'
9 'אין בכלל הכנסה'
1 'הרבה מתחת לממוצע'
2 'מתחת לממוצע'
3 'ממוצע'
4 'מעל הממוצע'
5 'הרבה מעל הממוצע'
6 'לא מעוניין לענות'.

*israel.
RECODE CBOR ('IL'=1) INTO rcbor.
*asia.
RECODE CBOR ('AF','BD','BN','BT','CN','HK','ID','IN','JP','KH','KP','KR','LA','LK','MM','MN','MO','MV','MY','NP','PH','PK','SG','TH','TL','TW','VN'=2) INTO rcbor.
*central america.
RECODE CBOR ('AG','AI','AN','AW','BB','BM','BS','CU','DM','DO','GD','GP','HT','JM','KN','KY','LC','MQ','MS','PR','TT','VC','BZ','CR','GT','HN','MX','NI','PA','SV'=3) INTO rcbor.
*eastern europe.
RECODE CBOR ('AL','BA','BG','CS','CY','CZ','GR','HR','HU','MK','PL','RO','SI','SK'=4) INTO rcbor.
*magreb.
RECODE CBOR ('DZ','EG','LY','MA','TN'=5) INTO rcbor.
*middle east.
RECODE CBOR ('AE','BH','IQ','IR','JO','KW','LB','OM','QA','SA','SY','TR','YE'=6) INTO rcbor.
*north america.
RECODE CBOR ('CA','US'=7) INTO rcbor.
*oceania.
RECODE CBOR ('AS','AU','CK','FJ','FM','GU','KI','MH','MP','NC','NR','NU','NZ','PF','PG','PN','PW','SB','TO','TV','VG','VI','VU','WS'=8) INTO rcbor.
*south america.
RECODE CBOR ('AR','BO','BR','CL','CO','EC','FK','GF','GY','PE','PY','SR','UY','VE','PG'=9) INTO rcbor.
*former ussr.
RECODE CBOR ('AM','AZ','BY','EE','GE','KG','KZ','LT','LV','MD','RU','TJ','TM','UA','UZ'=10) INTO rcbor.
*western europe.
RECODE CBOR ('AD','AT','BE','CH','DE','DK','ES','FI','FO','FR','GB','GI','GL','IE','IM','IS','IT','JE','LI','LU','MC','MT','NL','NO','PT','SE','SM'=11) INTO rcbor.
*africa.
RECODE CBOR ('AO','BF','BI','BJ','BW','CD','CF','CG','CI','CM','CV','DJ','EH','ER','ET','GA','GH','GM','GN','GQ','GW'=12) INTO rcbor.
RECODE CBOR ('KE','KM','LR','LS','MG','ML','MR','MU','MW','MZ','NA','NE','NG','RE','RW','SC','SD','SL','SN','SO','ST','SZ','TD','TG','TZ','UG','YT','ZA','ZM','ZW'=12) INTO rcbor.


VARIABLE LABELS rcbor 'יבשת לידה'.
VALUE LABELS rcbor
1 'ישראל'
2 'אסיה'
3 'מרכז אמריקה'
4 'מזרח אירופה'
5 'מגרב'
6 'המזרח התיכון'
7 'צפון אמריקה'
8 'אוקיאנייה'
9 'דרום אמריקה'
10 'ברית המועצות לשעבר'
11 'מערב אירופה'
12 'אפריקה'.
compute migzar = relid.
if rcbor=10 and alyayear>1989 migzar = 5.
if rel=3 or rel=4 migzar = 6.
if rel=2 and rcbor=1 migzar = 6.
VARIABLE LABELS migzar 'מגזר'.
VALUE LABELS migzar
1 'חילוניים'
2 'מסורתיים'
3 'דתיים'
4 'חרדים'
5 'רוסים'
6 'ערבים'.

VARIABLE LABELS vote2022 'הצבעה בבחירות נובמבר 2022 לפי רישום/סקר עדכון?'.
VALUE LABELS vote2022
1 'הליכוד'
2 'יש עתיד'
3 'הציונות הדתית'
4 'המחנה הממלכתי'
5 'שס'
6 'יהדות התורה'
7 'ישראל ביתנו'
8 'רע''מ'
9 'חד''ש/תע''ל'
10 'העבודה'
11 'מרצ'
12 'בל''ד'
13 'הבית היהודי'
14 'אחר'
15 'לא הצביע'
16 'צעיר מדי/לא יודע/מסרב לענות' .



