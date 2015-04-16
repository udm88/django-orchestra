# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billcontact',
            name='country',
            field=models.CharField(choices=[('KZ', 'Kazakhstan'), ('IM', 'Isle of Man'), ('VE', 'Venezuela (Bolivarian Republic of)'), ('PW', 'Palau'), ('WF', 'Wallis and Futuna'), ('HK', 'Hong Kong'), ('BO', 'Bolivia (Plurinational State of)'), ('RE', 'Réunion'), ('PS', 'Palestine, State of'), ('IE', 'Ireland'), ('CH', 'Switzerland'), ('AR', 'Argentina'), ('LA', "Lao People's Democratic Republic"), ('BA', 'Bosnia and Herzegovina'), ('IR', 'Iran (Islamic Republic of)'), ('BD', 'Bangladesh'), ('ER', 'Eritrea'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('SJ', 'Svalbard and Jan Mayen'), ('ZW', 'Zimbabwe'), ('IN', 'India'), ('TW', 'Taiwan (Province of China)'), ('DO', 'Dominican Republic'), ('PE', 'Peru'), ('HT', 'Haiti'), ('MO', 'Macao'), ('ST', 'Sao Tome and Principe'), ('VG', 'Virgin Islands (British)'), ('ME', 'Montenegro'), ('IT', 'Italy'), ('IQ', 'Iraq'), ('MT', 'Malta'), ('AG', 'Antigua and Barbuda'), ('UZ', 'Uzbekistan'), ('KN', 'Saint Kitts and Nevis'), ('TD', 'Chad'), ('AI', 'Anguilla'), ('MM', 'Myanmar'), ('AM', 'Armenia'), ('UY', 'Uruguay'), ('BB', 'Barbados'), ('BN', 'Brunei Darussalam'), ('CN', 'China'), ('AL', 'Albania'), ('AQ', 'Antarctica'), ('GT', 'Guatemala'), ('NR', 'Nauru'), ('UM', 'United States Minor Outlying Islands'), ('MP', 'Northern Mariana Islands'), ('SR', 'Suriname'), ('GY', 'Guyana'), ('LV', 'Latvia'), ('LS', 'Lesotho'), ('ES', 'Spain'), ('TC', 'Turks and Caicos Islands'), ('VA', 'Holy See'), ('NZ', 'New Zealand'), ('SK', 'Slovakia'), ('BE', 'Belgium'), ('TG', 'Togo'), ('SN', 'Senegal'), ('CG', 'Congo'), ('MN', 'Mongolia'), ('GA', 'Gabon'), ('GW', 'Guinea-Bissau'), ('HU', 'Hungary'), ('TR', 'Turkey'), ('GE', 'Georgia'), ('EH', 'Western Sahara'), ('PN', 'Pitcairn'), ('FJ', 'Fiji'), ('TV', 'Tuvalu'), ('AZ', 'Azerbaijan'), ('MZ', 'Mozambique'), ('GL', 'Greenland'), ('US', 'United States of America'), ('BF', 'Burkina Faso'), ('BT', 'Bhutan'), ('VN', 'Viet Nam'), ('PM', 'Saint Pierre and Miquelon'), ('PY', 'Paraguay'), ('FR', 'France'), ('DZ', 'Algeria'), ('LT', 'Lithuania'), ('NU', 'Niue'), ('MY', 'Malaysia'), ('DM', 'Dominica'), ('NC', 'New Caledonia'), ('NA', 'Namibia'), ('WS', 'Samoa'), ('MW', 'Malawi'), ('BW', 'Botswana'), ('SM', 'San Marino'), ('HM', 'Heard Island and McDonald Islands'), ('IS', 'Iceland'), ('CF', 'Central African Republic'), ('SB', 'Solomon Islands'), ('LK', 'Sri Lanka'), ('ID', 'Indonesia'), ('GR', 'Greece'), ('CO', 'Colombia'), ('MK', 'Macedonia (the former Yugoslav Republic of)'), ('KR', 'Korea (the Republic of)'), ('SZ', 'Swaziland'), ('KE', 'Kenya'), ('AF', 'Afghanistan'), ('AE', 'United Arab Emirates'), ('DK', 'Denmark'), ('TZ', 'Tanzania, United Republic of'), ('AD', 'Andorra'), ('KH', 'Cambodia'), ('CY', 'Cyprus'), ('GS', 'South Georgia and the South Sandwich Islands'), ('EG', 'Egypt'), ('UG', 'Uganda'), ('TK', 'Tokelau'), ('MS', 'Montserrat'), ('YT', 'Mayotte'), ('MU', 'Mauritius'), ('BS', 'Bahamas'), ('CD', 'Congo (the Democratic Republic of the)'), ('CZ', 'Czech Republic'), ('CR', 'Costa Rica'), ('NL', 'Netherlands'), ('GQ', 'Equatorial Guinea'), ('SS', 'South Sudan'), ('RW', 'Rwanda'), ('VU', 'Vanuatu'), ('DE', 'Germany'), ('PL', 'Poland'), ('CX', 'Christmas Island'), ('AO', 'Angola'), ('BZ', 'Belize'), ('CK', 'Cook Islands'), ('TO', 'Tonga'), ('MA', 'Morocco'), ('CU', 'Cuba'), ('JM', 'Jamaica'), ('NI', 'Nicaragua'), ('AT', 'Austria'), ('FI', 'Finland'), ('FO', 'Faroe Islands'), ('VI', 'Virgin Islands (U.S.)'), ('BR', 'Brazil'), ('SY', 'Syrian Arab Republic'), ('ET', 'Ethiopia'), ('BJ', 'Benin'), ('PH', 'Philippines'), ('AS', 'American Samoa'), ('TL', 'Timor-Leste'), ('AU', 'Australia'), ('SX', 'Sint Maarten (Dutch part)'), ('PG', 'Papua New Guinea'), ('NG', 'Nigeria'), ('SL', 'Sierra Leone'), ('LB', 'Lebanon'), ('OM', 'Oman'), ('SG', 'Singapore'), ('CM', 'Cameroon'), ('PT', 'Portugal'), ('KM', 'Comoros'), ('IO', 'British Indian Ocean Territory'), ('BM', 'Bermuda'), ('YE', 'Yemen'), ('RU', 'Russian Federation'), ('GM', 'Gambia'), ('SI', 'Slovenia'), ('GI', 'Gibraltar'), ('LY', 'Libya'), ('GU', 'Guam'), ('LU', 'Luxembourg'), ('RO', 'Romania'), ('MD', 'Moldova (the Republic of)'), ('BL', 'Saint Barthélemy'), ('GB', 'United Kingdom of Great Britain and Northern Ireland'), ('EE', 'Estonia'), ('LC', 'Saint Lucia'), ('TJ', 'Tajikistan'), ('IL', 'Israel'), ('PA', 'Panama'), ('PR', 'Puerto Rico'), ('CL', 'Chile'), ('KP', "Korea (the Democratic People's Republic of)"), ('GF', 'French Guiana'), ('CI', "Côte d'Ivoire"), ('MR', 'Mauritania'), ('NF', 'Norfolk Island'), ('BG', 'Bulgaria'), ('SD', 'Sudan'), ('NO', 'Norway'), ('GG', 'Guernsey'), ('CV', 'Cabo Verde'), ('GP', 'Guadeloupe'), ('BV', 'Bouvet Island'), ('TT', 'Trinidad and Tobago'), ('SO', 'Somalia'), ('DJ', 'Djibouti'), ('MC', 'Monaco'), ('JP', 'Japan'), ('NP', 'Nepal'), ('JE', 'Jersey'), ('TN', 'Tunisia'), ('RS', 'Serbia'), ('NE', 'Niger'), ('ML', 'Mali'), ('KW', 'Kuwait'), ('PF', 'French Polynesia'), ('ZA', 'South Africa'), ('GH', 'Ghana'), ('BH', 'Bahrain'), ('CC', 'Cocos (Keeling) Islands'), ('MQ', 'Martinique'), ('AW', 'Aruba'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('JO', 'Jordan'), ('LI', 'Liechtenstein'), ('TM', 'Turkmenistan'), ('MX', 'Mexico'), ('LR', 'Liberia'), ('GD', 'Grenada'), ('HN', 'Honduras'), ('SA', 'Saudi Arabia'), ('PK', 'Pakistan'), ('CA', 'Canada'), ('CW', 'Curaçao'), ('SV', 'El Salvador'), ('SC', 'Seychelles'), ('QA', 'Qatar'), ('EC', 'Ecuador'), ('VC', 'Saint Vincent and the Grenadines'), ('HR', 'Croatia'), ('MV', 'Maldives'), ('KI', 'Kiribati'), ('FM', 'Micronesia (Federated States of)'), ('BY', 'Belarus'), ('FK', 'Falkland Islands  [Malvinas]'), ('TF', 'French Southern Territories'), ('AX', 'Åland Islands'), ('MG', 'Madagascar'), ('SE', 'Sweden'), ('BI', 'Burundi'), ('KY', 'Cayman Islands'), ('MF', 'Saint Martin (French part)'), ('ZM', 'Zambia'), ('GN', 'Guinea'), ('UA', 'Ukraine'), ('TH', 'Thailand'), ('KG', 'Kyrgyzstan'), ('MH', 'Marshall Islands')], verbose_name='country', max_length=20, default='ES'),
        ),
        migrations.AlterField(
            model_name='billline',
            name='tax',
            field=models.DecimalField(decimal_places=2, verbose_name='tax', max_digits=4),
        ),
    ]