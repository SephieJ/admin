# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import FileField
from wtforms import TextAreaField
from wtforms.validators import InputRequired
from wtforms.validators import Optional , Length
from wtforms import SelectField
from app.src.utils.helpers import (
    special_chars, sg_mobile_number, sg_office_number)
from wtforms import SubmitField

class CompanyForm(FlaskForm):
    # name = StringField(validators=[InputRequired('Company Name is required')])
    # company_info = TextAreaField(validators=[InputRequired('Company Information is required')])
    # business_reg_number = StringField(validators=[InputRequired('Business Reg Number is required')])
    # office_number = StringField(validators=[InputRequired('Office Number is required')])
    # mobile_number = StringField(validators=[InputRequired('Mobile Number is required')])    
    # latitude = StringField(validators=[Optional()])
    # longitude = StringField(validators=[Optional()])
    # block_street = StringField(validators=[InputRequired('Blockstreet is required')])
    # postal_code = StringField(validators=[InputRequired('Postal Code is required')])

    name = StringField(validators=[
        InputRequired("Company name is required."), special_chars()])
    company_info = TextAreaField(validators=[
        Optional(),
        Length(
          min=0, max=250)])

    business_reg_number = StringField(validators=[Optional()])
    office_number = StringField(validators=[
        Optional(),
        sg_office_number(),
        Length(
            min=8, max=8,
            message='Phone number should be 8 digits.')])
    mobile_number = StringField(validators=[
        Optional(),
        sg_mobile_number(),
        Length(
            min=8, max=8,
            message='Mobile number should be 8 digits.')])
    company_industry = SelectField(coerce=int, validators=[Optional()])
    industry = SelectField(validators=[
        Optional()],
        choices=[(4, 'Consumer Business'), (6, 'Design'), (13, 'Others'),
                 (14, 'Food and Beverage'), (15, 'Information Technology'),
                 (16, 'Media'), (17, 'Aerospace Engineering'),
                 (18, 'Automotive'), (19, 'Chemicals'),
                 (21, 'Content and Media'), (23, 'Electronics'),
                 (24, 'Energy'), (25, 'F&B'), (26, 'Industrial Solutions'),
                 (27, 'Infocomm Services'), (28, 'Information Tech'),
                 (29, 'Landscape'), (30, 'Lifestyle Products and Services'),
                 (31, 'Logistics and Supply Chain Management'),
                 (32, 'Manufacturing'), (33, 'Maritime'),
                 (34, 'Marine and Offshore Engineering'),
                 (35, 'Medical Technology'), (36, 'Natural Resources'),
                 (37, 'Oil and Gas Equipment and Services'),
                 (38, 'Pharmaceuticals and Biotechnology'),
                 (39, 'Precision Engineering'), (40, 'Retail'),
                 (41, 'Robotics'), (42, 'Safety and Security'),
                 (44, 'Space'), (45, 'Tourisim'),
                 (46, 'Urban Solutions and Sustainability')])
    company_size = SelectField(validators=[
        Optional()],
        choices=[('LT10', '< 10'), ('TTOF', '10 - 50'),
                 ('F1TO1H', '51 to 100'), ('H1TO2H', '101 - 200'),
                 ('GT2H', '> 200')])
    company_revenue = SelectField(validators=[
        Optional()],
        choices=[('LTONEM', '< $1 Mil'), ('ONEMTOTENM', '$1 - $10 Mil'),
                 ('ELEVENMTO1HM', '$11 - $100 Mil'), ('GT1HM', '> $100 Mil')])
    company_years = SelectField(validators=[
        Optional()],
        choices=[('LT2Y', '< 2 years'), ('TTOFY', '3 - 5 years'),
                 ('STO10Y', '6 - 10 years'), ('STO10Y', 'GT10Y'),
                 ('NA', 'N.A.')])
    iso = SelectField(validators=[
        Optional()],
        choices=[('AS 9100 Aerospace', 'AS 9100 Aerospace'),
                 ('ISO 9001 Quality Management',
                  'ISO 9001 Quality Management'),
                 ('ISO 13485 Medical Devices',
                  'ISO 13485 Medical Devices'),
                 ('ISO 14001 Environmental Management',
                  'ISO 14001 Environmental Management'),
                 ('ISO/IEC 17025 Testing and Calibration Laboratories',
                  'ISO/IEC 17025 Testing and Calibration Laboratories'),
                 ('OHSAS 18001/SS 506 Safety and Health',
                  'OHSAS 18001/SS 506 Safety and Health'),
                 ('ISO 20121 Sustainable Events',
                  'ISO 20121 Sustainable Events'),
                 ('ISO 22000 Food safety Management',
                  'ISO 22000 Food safety Management'),
                 ('ISO 22301 Business Continuity Management',
                  'ISO 22301 Business Continuity Management'),
                 ('ISO/IEC 27001 Information Security Management',
                  'ISO/IEC 27001 Information Security Management'),
                 ('ISO 29990 Learning Service Provider',
                  'ISO 29990 Learning Service Provider'),
                 ('ISO 26000 Social Responsibility',
                  'ISO 26000 Social Responsibility'),
                 ('ISO 31000 Risk Management',
                  'ISO 31000 Risk Management'),
                 ('ISO 45001 Occupational Health and Safety',
                  'ISO 45001 Occupational Health and Safety'),
                 ('ISO 50001 Energy Management',
                  'ISO 50001 Energy Management'),
                 ('SS 587 End-of-Life ICT Equipment',
                  'SS 587 End-of-Life ICT Equipment'),
                 ('SS577 Water Efficiency', 'SS577 Water Efficiency')])
    bca = SelectField(validators=[
        Optional()],
        choices=[('CW01 - General Building', 'CW01 - General Building'),
                 ('CW02 - Civil Engineering', 'CW02 - Civil Engineering'),
                 ('CR01 - Minor Construction Work',
                  'CR01 - Minor Construction Work'),
                 ('CR02 - Corrosion Protection',
                  'CR02 - Corrosion Protection'),
                 ('CR03 - Demolition', 'CR03 - Demolition'),
                 ('CR04 - Fencing & Ironworks', 'CR04 - Fencing & Ironworks'),
                 ('CR05 - Concrete Repairs', 'CR05 - Concrete Repairs'),
                 ('CR06 - Interior Decoration & Finishing Works',
                  'CR06 - Interior Decoration & Finishing Works'),
                 ('CR07 - Cable/Pipe Laying & Road Reinstatement',
                  'CR07 - Cable/Pipe Laying & Road Reinstatement'),
                 ('CR08 - Piling Works', 'CR08 - Piling Works'),
                 ('CR09 - Repairs & Redecoration',
                  'CR09 - Repairs & Redecoration'),
                 ('CR10 - Pre-cast Concrete Works',
                  'CR10 - Pre-cast Concrete Works'),
                 ('CR11 - Signcraft Installation',
                  'CR11 - Signcraft Installation'),
                 ('CR12 - Ground Support & Stabilisation Works',
                  'CR12 - Ground Support & Stabilisation Works'),
                 ('CR13 - Waterproofing Installation',
                  'CR13 - Waterproofing Installation'),
                 ('CR14 - Asphalt Works & Road Marking',
                  'CR14 - Asphalt Works & Road Marking'),
                 ('CR15 - Site Investigation Works',
                  'CR15 - Site Investigation Works'),
                 ('CR16 - Curtain Walls', 'CR16 - Curtain Walls'),
                 ('CR17 - Windows', 'CR17 - Windows'),
                 ('CR18 - Doors', 'CR18 - Doors'),
                 ('MW02 - Housekeeping, Cleansing, \
                  Desilting & Conservancy Service',
                  'MW02 - Housekeeping, Cleansing, \
                  Desilting & Conservancy Service'),
                 ('MW03 - Landscaping', 'MW03 - Landscaping'),
                 ('MW04 - Pest Control', 'MW04 - Pest Control'),
                 ('ME01 - Air-Conditioning, Refrigeration & Ventilation Works',
                  'ME01 - Air-Conditioning, Refrigeration \
                  & Ventilation Works'),
                 ('ME02 - Building Automation, Industrial \
                  & Process Control Systems',
                  'ME02 - Building Automation, Industrial \
                  & Process Control Systems'),
                 ('ME03 - Solar PV System Integration',
                  'ME03 - Solar PV System Integration'),
                 ('ME04 - Communication & Security Systems',
                  'ME04 - Communication & Security Systems'),
                 ('ME05 - Electrical Engineering',
                  'ME05 - Electrical Engineering'),
                 ('ME06 - Fire Prevention & Protection Systems',
                  'ME06 - Fire Prevention & Protection Systems'),
                 ('ME07 - High & Low Tension Overhead Line Installation',
                  'ME07 - High & Low Tension Overhead Line Installation'),
                 ('ME08 - Internal Telephone Wiring for Telecommunications',
                  'ME08 - Internal Telephone Wiring for Telecommunications'),
                 ('ME09 - Lift & Escalator Installation',
                  'ME09 - Lift & Escalator Installation'),
                 ('ME10 - Line Plant Cabling/Wiring for Telecommunications',
                  'ME10 - Line Plant Cabling/Wiring for Telecommunications'),
                 ('ME11 - Mechanical Engineering',
                  'ME11 - Mechanical Engineering'),
                 ('ME12 - Plumbing & Sanitary Works',
                  'ME12 - Plumbing & Sanitary Works'),
                 ('ME13 - Traffic Light Systems',
                  'ME13 - Traffic Light Systems'),
                 ('ME14 - Underground Pipleline for Telecommunications',
                  'ME14 - Underground Pipleline for Telecommunications'),
                 ('ME15 - Integrated Building Services',
                  'ME15 - Integrated Building Services'),
                 ('RW01 - Window Contractors', 'RW01 - Window Contractors'),
                 ('RW02 - Lift Contractors', 'RW02 - Lift Contractors'),
                 ('RW03 - Escalator Contractors',
                  'RW03 - Escalator Contractors'),
                 ('SY01A - Essential Construction Materials',
                  'SY01A - Essential Construction Materials'),
                 ('SY01B - Ready-Mixed Concrete',
                  'SY01B - Ready-Mixed Concrete'),
                 ('SY01C - Other Basic Construction Materials',
                  'SY01C - Other Basic Construction Materials'),
                 ('SY02 - Chemicals', 'SY02 - Chemicals'),
                 ('SY04 - Electrical Equipment',
                  'SY04 - Electrical Equipment'),
                 ('SY05 - Electrical & Electronic Materials, \
                  Products & Components',
                  'SY05 - Electrical & Electronic Materials, \
                  Products & Components'),
                 ('SY06 - Finishing & Building Products',
                  'SY06 - Finishing & Building Products'),
                 ('SY07 - Gases', 'SY07 - Gases'),
                 ('SY08 - Mechanical Equipment, Plant & Machinery',
                  'SY08 - Mechanical Equipment, Plant & Machinery'),
                 ('SY09 - Mechanical Materials Products & Components',
                  'SY09 - Mechanical Materials Products & Components'),
                 ('SY10 - Metal & Timber Structures',
                  'SY10 - Metal & Timber Structures'),
                 ('SY11 - Petroleum Products', 'SY11 - Petroleum Products'),
                 ('SY12 - Pipes', 'SY12 - Pipes'),
                 ('SY14 - Sanitary Products', 'SY14 - Sanitary Products'),
                 ('TR01 - Formwork', 'TR01 - Formwork'),
                 ('TR02 - Steel Reinforcement Work',
                  'TR02 - Steel Reinforcement Work'),
                 ('TR03 - Concreting Work', 'TR03 - Concreting Work'),
                 ('TR04 - Drywall Installation',
                  'TR04 - Drywall Installation'),
                 ('TR05 - Pre-cast Installation',
                  'TR05 - Pre-cast Installation'),
                 ('TR06 - Ceiling Work', 'TR06 - Ceiling Work'),
                 ('TR07 - Tile/Marble/Stone Work',
                  'TR07 - Tile/Marble/Stone Work'),
                 ('TR08 - Timber, Vinyl and Laminate Flooring Works',
                  'TR08 - Timber, Vinyl and Laminate Flooring Works'),
                 ('TR09 - Plastering/Skimming', 'TR09 - Plastering/Skimming'),
                 ('TR10 - Ironmongery & Metalwork',
                  'TR10 - Ironmongery & Metalwork'),
                 ('GB1 - General Builder Class 1',
                  'GB1 - General Builder Class 1'),
                 ('GB2 - General Builder Class 2',
                  'GB2 - General Builder Class 2')
                 # ('SB(GS) - Specialist Builder \
                 #  (Ground Support and Stabilisation Works)',
                 #  'SB(GS) - Specialist Builder \
                 #  (Ground Support and Stabilisation Works)'),
                 # ('SB(PC) - Specialist Builder (Pre-cast Concrete Work)'
                 #  'SB(PC) - Specialist Builder (Pre-cast Concrete Work)'),
                 # ('SB(PT) - Specialist Builder (In-situ Post-tensioning Work)',
                 #  'SB(PT) - Specialist Builder \
                 #  (In-situ Post-tensioning Work)'),
                 # ('SB(PW) - Specialist Builder (Piling Works)',
                 #  'SB(PW) - Specialist Builder (Piling Works)'),
                 # ('SB(SI) - Specialist Builder (Site Investigation Work)',
                 #  'SB(SI) - Specialist Builder (Site Investigation Work)'),
                 # ('SB(SS) - Specialist Builder (Structural SteelWork)',
                 #  'SB(SS) - Specialist Builder (Structural SteelWork)')
                 ])
    bizsafe = SelectField(validators=[
        Optional()],
        choices=[('LEVEL1', 'BizSafe Level 1'),
                 ('LEVEL2', 'BizSafe Level 2'),
                 ('LEVEL3', 'BizSafe Level 3'),
                 ('LEVEL4', 'BizSafe Level 4'),
                 ('LEVELSTAR', 'BizSafe Level Star')])
    website = StringField(validators=[Optional()])
    facebook = StringField(validators=[Optional()])
    linkedin = StringField(validators=[Optional()])
    block_street = StringField(validators=[Optional()])
    postal_code = StringField(validators=[Optional()])
    latitude = StringField(validators=[Optional()])
    longitude = StringField(validators=[Optional()])
    accreditations = StringField(validators=[Optional()])
    unit_number = StringField(validators=[Optional()])
    image_url = FileField(validators=[Optional()])
    save = SubmitField('Save')
