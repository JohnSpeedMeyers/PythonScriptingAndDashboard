# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 18:27:13 2018
@authors: Ben Smith (bsmith@rand.org), Juliana Chen (jchenper@rand.org),
Sangita Baxi (sbaxi@rand.org), John Speed Meyers (jmeyers@rand.org)


Project: Opioid Hackathon
Team 1
Sub-Task 1

Description: Import raw treatment center dataset. Create labels for relevant
codes. This files creates a dataset that that makes mapping and visualization
straightforward.

Note: Check out these commands

## apply function -- check this
## df.groupby("year").get_group(2012) -- check this
## code-year dictionary


"""

## Import some modules to ease data analysis
import pandas as pd
import numpy  as np

## Import treatment center dataset
## This dataset will eventually reside on our git. We will have to change
## the address below.
df = pd.read_csv(r"~\Desktop\Opioid Hackathon\data\treatmentCenterData.csv")

## For info on coding decisions made below, see the team's spreadsheet
## called treatment_center_labels.xlsx. There are many ambiguities in the
## labeling. We have attempted to be explicit where we made judgements.
## I set values to nan (not a number - aka missing) when it was hard to tell
## what to do.

## Set to one if year-code combinations exist and zero otherwise
## For regular expressions, I used the logic that either that services_raw
## column must either be only that acronym, begin with the particular acronym
## and have a space, or there must be a space and then the acronym and then a 
## space or the acronym should be at the end of the column
## For a helpful python regex cheat sheet, see
## https://www.debuggex.com/cheatsheet/regex/python

## Create focus on substance abuse treatment services dummy
df['focus_sats'] = np.where(
        ((df.year <= 2013) & 
        df.services_raw.str.contains("^SA$|^SA | SA | SA$")) |
        (((df.year >= 2015) & (df.year <= 2017)) &
        df.services_raw.str.contains("^SAF$|^SAF | SAF | SAF$")), 
        1, np.where((df.year == 2014) | (df.year == 2018), np.nan, 0))

## Create focus on mental health services dummy
df['focus_mhs'] = np.where(
        ((df.year <= 2013) & 
        df.services_raw.str.contains("^MH$|^MH | MH | MH$")) |
        (((df.year >= 2015) & (df.year <= 2017)) &
        df.services_raw.str.contains("^MHF$|^MHF | MHF | MHF$")), 
        1, np.where((df.year == 2014) | (df.year == 2018), np.nan, 0))
                 
## Create a focus on mental health and substance abuse treatment services dummy
df['focus_mhsats'] = np.where(
        ((df.year <= 2013) & 
        df.services_raw.str.contains("^MH-SA$|^MH-SA | MH-SA | MH-SA$")) |
        (((df.year >= 2015) & (df.year <= 2017)) &
        df.services_raw.str.contains("^MHSAF$|^MHSAF | MHSAF | MHSAF$")), 
        1, np.where((df.year == 2014) | (df.year == 2018), np.nan, 0))
        
## Create a focus on general health services dummy
## Where year is less than 2013 and string containts X OR where year
## is between 2015 and 2017 and string contains X replace with 1
## otherwise where the year is 2014 or 2018 replace with nan otherwise 0?z
df['focus_ghs'] = np.where(
        ((df.year <= 2013) & 
        df.services_raw.str.contains("^GH$|^GH | GH | GH$")) |
        (((df.year >= 2015) & (df.year <= 2017)) &
        df.services_raw.str.contains("^GHF$|^GHF | GHF | GHF$")), 
        1, np.where((df.year == 2014) | (df.year == 2018), np.nan, 0))
        
## Run check that the "focus" variables above are mutually exclusive and
## completely exhaustive
# df['check'] = df.focus_sats + df.focus_mhs + df.focus_mhsats + df.focus_ghs
## 166,063 treatment centers fall into one of these four categories
## Results: No double-counting, therefore mutually exclusive
## Results: Not completely exhaustive, there are some centers with none of 
## these labels
        
## Show first ten rows
print(df.head())

######################################
#------TREATMENT SETTING -------------
######################################

#----- Actual Codes -------------------
# Outpatient	OP
# Partial hospitalization/day treatment	PH
# Non-hospital residential (24-hour)	RR
# Hospital inpatient	HI
# Residential short-term treatment (30 days or less)	RS
# Residential long-term treatment (more than 30 days)	RL
# Computerized Treatment	CT
# Hospital Inpatient Detoxification	HID
# Hospital Inpatient Treatment	HIT
# Outpatient Detoxification	OD
# Outpatient Day Treatment or Partial Hospitalization	ODT
# Intensive Outpatient Treatment	OIT
# Outpatient Methadone/Buprenorphine or Vivitrol	OMB
# Regular Outpatient Treatment	ORT
# Residential Detoxification	RD
# Residential	RES
# Psychiatric Hospital	PSYH
# General Hospital (Including VA Hospital)	GH

#---- Proposed Grouping ----------------
# Hospital Inpatient (HI+HID+HIT)
# Residential (RR+RS+RL+RD+RES)
# Outpatient (OP+OD+OIT+OMB+ORT)
# Day Treatment/Partial Hospital (PH+ODT)
# Computer (CT)
# Ignore PSYH and GH for now 

#-----------------
# My thought here was that, over time, these codes seem to conflate 
# setting and treatment. I opted to focus and group based on setting and
# I ignored GH and PSYH entirely because I think they fit better in
# other categories. 
#-----------------

# Hospital Inpatient (HI+HID+HIT)
## Note: This grouping combines hospital inpatient, hospital inpatient treatment
## and hospital inpatient detoxification.
df['setting_hi'] = np.where(
        df.services_raw.str.contains(
                "^HID?T? | HID?T? | HID?T?$"), 
                1, 0)

df['setting_res'] = np.where(
        df.services_raw.str.contains(
                "^RR?S?L?D?| RR?S?L?D? | RR?S?L?D?$ |^RES| RES | RES$"), 
                1, 0)

df['setting_op'] = np.where(
        df.services_raw.str.contains(
                "^OP?D?(IT)?(MB)?(RT)?| OP?D?(IT)?(MB)?(RT)? | OP?D?(IT)?(MB)?(RT)?$"), 
                1, 0)
        
df['setting_dtph'] = np.where(
        df.services_raw.str.contains(
                "^PH| PH | PH$|^ODT| ODT | ODT$"), 
                1, 0)

df['setting_ct'] = np.where(
        df.services_raw.str.contains(
                "^CT| CT | CT$"), 
                1, 0)
        
## Quick check that it's coding things correctly      
#df.loc[135110:135120,'setting_op']

######################################
#------PAYER MIX ---------------------
######################################

#----- Actual Codes --------------
# Access to recovery (ATR) voucher	AR or ATR
# Federal, or any government funding for substance abuse programs	FSA 
# IHS/Tribal/Urban (ITU) funds	ITU 
# Medicare	MC 
# Medicaid	MD 
# Military insurance (e.g., TRICARE)	MI 
# No payment accepted	NP 
# Private health insurance	 PI 
# Cash or self-payment	SF 
# State financed health insurance plan other than Medicaid	SI 
# IHS/638 Contract Care Funds	IH or IHS


#----- Proposed Codes ------------
# Same as above.
# Could potentially combine IHS and ITU but have not done so at this time.

#-----------------
# Here the problem is that some of the codes change across years but
# still refer to the same payment source. (e.g. AR->ATR)
#-----------------


df['payment_atr'] = np.where(
        df.services_raw.str.contains(
                "^AT?R| AT?R | AT?R$"),
                1,0)
        
df['payment_mc'] = np.where(
        df.services_raw.str.contains(
                "^MC | MC | MC$"),
                1,0)
        
df['payment_md'] = np.where(
        df.services_raw.str.contains(
                "^MD | MD | MD$"),
                1,0)
    
df['payment_mi'] = np.where(
        df.services_raw.str.contains(
                "^MI | MI | MI$"),
                1,0)
        
df['payment_pi'] = np.where(
        df.services_raw.str.contains(
                "^PI | PI | PI$"),
                1,0)

df['payment_sf'] = np.where(
        df.services_raw.str.contains(
                "^SF | SF | SF$"),
                1,0)
        
df['payment_si'] = np.where(
        df.services_raw.str.contains(
                "^SI | SI | SI$"),
                1,0)

# IH in 2016 and beyond is a Facility Operation code for Indian Health Service 
df['payment_ihs'] = np.where(
        (df.year >= 2013) & (df.year <= 2015) & df.services_raw.str.contains(
                "^IHS? | IHS? | IHS?$"),
                1, 0)

df['payment_itu'] = np.where(
        (df.year >= 2016) & (df.year <= 2018) & df.services_raw.str.contains(
                "^ITU | ITU | ITU$"),
                1, 0)
        
df['payment_fsa'] = np.where(
        (df.year >= 2016) & (df.year <= 2018) & df.services_raw.str.contains(
                "^FSA | FSA | FSA$"),
                1, 0)
        
df['payment_np'] = np.where(
        (df.year >= 2014) & (df.year <= 2018) & df.services_raw.str.contains(
                "^NP | NP | NP$"),
                1, 0)


######################################
#------LANGUAGE SERVICES -------------
######################################

#----- Actual Codes --------------
# ASL or other assistance for hearing impaired AH
# Spanish SP
# Amerindian Languages NXXX (Not going to list but dozens)
# Other Languages FXXX (Not going to list but dozens)


#----- Proposed Codes ------------
# ASL or other assistance for hearing impaired AH
# Spanish SP
# Amerindian Languages NA
# Chinese CH
# Tagalog TA
# Vietnamese VI
# Other Languages OT 

#-----------------
# Want to condense dozens of language codes into 4
#-----------------

# Need to check for any inconsistent coding across years

df['language_ah'] = np.where(
        df.services_raw.str.contains(
                "^AH | AH | AH$"),
                1,0)

df['language_sp'] = np.where(
        df.services_raw.str.contains(
                "^SP| SP | SP$"),
                1,0)
                
df['language_na'] = np.where(
        df.services_raw.str.contains(
                "^N\d{1,3} | N\d{1,3}  | N\d{1,3} $"),
                1,0)
    
df['language_ch'] = np.where(
         ((df.year == 2003) &
         df.services_raw.str.contains("F14")) |
         ((df.year == 2004) &
         df.services_raw.str.contains("F60")) |
         ((df.year == 2005) &
         df.services_raw.str.contains("F11")) |
         ((df.year >= 2006) &
         df.services_raw.str.contains("F17")),1,0)

df['language_ta'] = np.where(
         ((df.year == 2001) & 
         df.services_raw.str.contains("F58")) |
         ((df.year == 2003) &
         df.services_raw.str.contains("F99")) |
         ((df.year == 2004) &
         df.services_raw.str.contains("F325"))|
         ((df.year == 2005) &
         df.services_raw.str.contains("F64")) |
         ((df.year == 2006) &
         df.services_raw.str.contains("F79")) |
         ((df.year >= 2007) &
         df.services_raw.str.contains("F81")),1,0)

df['language_vi'] = np.where(
         ((df.year == 2001) & 
         df.services_raw.str.contains("F63")) |
         ((df.year == 2003) &
         df.services_raw.str.contains("F109")) |
         ((df.year == 2004) &
         df.services_raw.str.contains("F370"))|
         ((df.year == 2005) &
         df.services_raw.str.contains("F72")) |
         ((df.year == 2006) &
         df.services_raw.str.contains("F90")) |
         ((df.year >= 2007) &
         df.services_raw.str.contains("F92")),1,0)

# Need to remove previous languages from "other languages" category?
         
df['language_ot'] = np.where(
        df.services_raw.str.contains(
                "^F\d{1,3} | F\d{1,3}  | F\d{1,3} $"),
                1,0)
        

######################################
#------TREATMENT VARIABLES------------
######################################
        
#----- Actual Codes --------------

## METHADONE GROUPRING
## ML - 2001 - Methadone/LAAM
## MM - 2003 - 2018 - Methadone/LAAM maintenance
## DM - 2003 - 2018 - Methadone/LAAM detoxification
## MMW - 2016 - 2018 - Methadone Maintenance for predetermined time
## METH - 2018 - Methadone
## MU - 2018 - Methadone used in treatment

## BUPRENORPHINE GROUPING
## BU - 2007 - 2018 - Buprenorphine
## BMW - 2016 - 2018 - Buprenorphine Maintenance for Predetermined Time
## BM - 2016, 2018 - Buprenorphone Maintenance
## DB - 2016 - 2018 - Buprehorphone detoxification
## BM - 2017 - Buprenoprhine maintenance
## BWON - 2018 - Buprenorphone withou naxalone (Suboxone)
## BSDM - 2018 - Buprenophine sub-dermal implant (Probuphine)
## BWN - 2018 - Buprenorphine with naxolone

## NALTREXONE GROUPING
## NXN - 2014 - 2018 - Naltrexone
## RPM - 2016 - 2018 - Relapse prevention with Naltrexone
## VTRL - 2014 - 2018 - Vivitrol (injectable Naltrexone)
## NU - 2018 - Naltrexone used in treatment

## ACAMPROSATE
## ACM - 2017 - 2018 - Acamprosate

## DISULFRAM
## DSF - 2017 - 2018 - Disulfram (Antabuse)
        
## All methadone treatment codes   
df['methadone'] = np.where(
        ((df.year == 2001) & 
        df.services_raw.str.contains("^ML$|^ML | ML | ML$")) |
        (((df.year >= 2003) & (df.year <= 2018)) &
        df.services_raw.str.contains("^MM$|^MM | MM | MM$")) |
        (((df.year >= 2003) & (df.year <= 2018)) &
        df.services_raw.str.contains("^DM$|^DM | DM | DM$")) |
        (((df.year >= 2016) & (df.year <= 2018)) &
        df.services_raw.str.contains("^MMW$|^MMW | MMW | MMW$")) |
        ((df.year == 2018)  &
        df.services_raw.str.contains("^METH$|^METH | METH | METH$")) |
        ((df.year == 2018) &
        df.services_raw.str.contains("^MU$|^MU | MU | MU$")), 
        1, 0)

## All buprenorphine treatment codes
df['buprenorphine'] = np.where(
        (((df.year >= 2007) & (df.year <= 2018)) &
        df.services_raw.str.contains("^BU$|^BU | BU | BU$")) |
        (((df.year >= 2016) & (df.year <= 2018)) &
        df.services_raw.str.contains("^BMW$|^BMW | BMW | BMW$")) |
        (((df.year >= 2016) & (df.year <= 2018)) &
        df.services_raw.str.contains("^BM$|^BM | BM | BM$")) |
        (((df.year >= 2016) & (df.year <= 2018)) &
        df.services_raw.str.contains("^DB$|^DB | DB | DB$")) |
        ((df.year == 2018) &
        df.services_raw.str.contains("^BWON$|^BWON | BWON | BWON$")) |
        ((df.year == 2018) &
        df.services_raw.str.contains("^BSDM$|^BSDM | BSDM | BSDM$")) |
        ((df.year == 2018) &
        df.services_raw.str.contains("^BWN$|^BWN | BWN | BWN$")), 
        1, 0)    

## All naltrexone treatment codes
df['naltrexone'] = np.where(
        (((df.year >= 2014) & (df.year <= 2018)) &
        df.services_raw.str.contains("^NXN$|^NXN | NXN | NXN$")) |
        (((df.year >= 2016) & (df.year <= 2018)) &
        df.services_raw.str.contains("^RPN$|^RPN | RPN | RPN$")) |
        (((df.year >= 2014) & (df.year <= 2018)) &
        df.services_raw.str.contains("^VTRL$|^VTRL | VTRL | VTRL$")) |
        ((df.year == 2018) &
        df.services_raw.str.contains("^NU$|^NU | NU | NU$")), 
        1, 0)    
        
## All acamprosate treatment codes
df['acamprosate'] = np.where(
        ((df.year == 2018) &
        df.services_raw.str.contains("^ACM$|^ACM | ACM | ACM$")), 
        1, 0)  
        
## All Disulfram (Antabuse) treatment codes
df['disulfram'] = np.where(
        ((df.year == 2018) &
        df.services_raw.str.contains("^DSF$|^DSF | DSF | DSF$")), 
        1, 0)        
        

######################################
#------MISC PROGRAMS------------------
######################################


        
#----- Proposed Codes ------------


#-----------------
# Want to condense dozens of language codes into 4
#-----------------

# One or more of LGBTQ
# People with HIV AIDS
# Methodone used in any type of treatment (combine all methodone mentions)
# Buprenorphin used in any type of treatment (combine all bup mentions)
# Naltrexone used in any type of treatment
        

######################################
#------EXPORT TO CSV------------------
######################################
        
df.to_csv(r"~\Desktop\Opioid Hackathon\data\treatmentCenterData_cleaned.csv")
