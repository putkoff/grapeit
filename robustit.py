from module_test.excel_module import *
import pandas as pd
import os
import re
def extract_zip_codes(text):
    """
    Extracts all ZIP codes from the provided text.
    ZIP codes are expected to be in the format 12345 or 12345-6789.
    """
    zip_pattern = re.compile(r'\b\d{5}(?:-\d{4})?\b')
    zip_codes = zip_pattern.findall(text)
    return zip_codes

def extract_city_names(text):
    """
    Extracts all city names from the provided text.
    Assumes city names are in all caps followed by one or more ZIP codes.
    """
    city_pattern = re.compile(r'([A-Z\s]+)\s\d{5}(?:[-\s,]*\d{5})*')
    cities = city_pattern.findall(text)
    cities = [city.strip() for city in cities]  # Clean extra whitespace
    return cities

def extract_emails(text, patterns):
    """
    Extracts email addresses from provided text using a list of regex patterns.
    """
    for pattern in patterns:
        emails = re.findall(pattern, text, re.IGNORECASE)
        if emails:
            return emails  # Returns list of emails as soon as any valid pattern matches
    return []  # Return an empty list if no patterns match
def compare_strings(s1, s2):
    """
    Compares two strings to check if they are the same length and identical in all characters
    except possibly within numeric characters. Returns the differing numbers if found.

    Parameters:
        s1 (str): The first string to compare.
        s2 (str): The second string to compare.

    Returns:
        tuple: (bool, list) where bool indicates if the strings match under the given conditions,
               and list contains the pairs of differing numbers if any.
    """
    
    # Check if the strings are the same length
    if len(s1) != len(s2):
        return (False, [])

    # Find all numbers in both strings
    numbers_s1 = re.findall(r'\d+', s1)
    numbers_s2 = re.findall(r'\d+', s2)

    # Replace digits in both strings with '0' to compare non-numeric parts
    transformed_s1 = re.sub(r'\d', '0', s1)
    transformed_s2 = re.sub(r'\d', '0', s2)

    if transformed_s1 != transformed_s2:
        return (False, [])

    # Comparing the numbers in the same order they appear
    differing_numbers = []
    for num1, num2 in zip(numbers_s1, numbers_s2):
        if num1 != num2:
            differing_numbers.append((num1, num2))

    # If the non-numeric parts are identical and the numeric parts have differences
    if differing_numbers:
        return (True, differing_numbers)
    else:
        # If there are no numeric differences
        return (True, [])
def replace_list(list_objs,string):
    for list_obj in list_objs:
        string = string.replace(list_obj,'')
    return string
def get_most_original_from_ls(string, values_list,string_list):
    strings = [string,'']
    for string_2 in values_list:
        strings[1] = string_2
        bool_comp,string_comp = compare_strings(string, string_2)
        
        if bool_comp and string_comp and bool_comp not in string_list:
            lowest = None
            for i,each in enumerate(string_comp[0]):
                each=int(each)
                if lowest == None or lowest[1] > each:
                    lowest=[i,each]
            return strings[lowest[0]]
    return string
def get_closest_headers(df,list_obj):
    dicts = get_df(df)
    headers = get_column_headers(df)
    closest_js = {key:"" for key in list_obj}
    for key,values in closest_js.items():
        for comp_key in headers:
            if comp_key.lower() == key:
                closest_js[key]=comp_key
                break
        if closest_js[key] == "":
            matches = {}
            for comp_key in headers:
                if comp_key not in list(closest_js.values()):
                    for char in key:
                        if char in comp_key.lower():
                            if comp_key not in matches:
                                matches[comp_key]=[]
                            if len(matches[comp_key])==0:
                                matches[comp_key].append('')
                            if matches[comp_key][-1]+char in comp_key.lower():
                                matches[comp_key][-1]+=char
                            else:
                                matches[comp_key].append(char)
    
            for header,values in matches.items():
                len_header = len(header)
                highest=[0,'']
                for val in values:
                    if len(val)>highest[0]:
                        highest=[len(val),val]
                matches[header]={'perc':highest[0]/len_header,'value':highest[1]}
            highest=[0,'']
            for header,val in matches.items():
                if val['perc']>highest[0]:
                    highest=[val['perc'],header]
            closest_js[key] = get_most_original_from_ls(highest[-1],headers, closest_js.values())
    return closest_js

# Define multiple email patterns
def choose_parser(header,df,query):
    parsers={"email":[r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',r'^\S+@\S+\.\S+$'],
    "phones":[r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',r'\(?\d{3}\)?[-.\s]?\d{7}',r'\b\d{10}\b',r'\b\d{7}\b'],
    "city":[r'([A-Z\s]+)\s\d{5}(?:[-\s,]*\d{5})*'],
    'zip':[r'\b\d{5}\b'],
    'fico':[r'\b\d{3}\b'],
    'combined heloc & mortgage balanced':[r'\b\d{6}\b'],
    'mtg10':[r'\b\d{6}\b'],
    'state':[r'\b[A-Z]{2}\b']}
    df = get_df(df)
    parse_keys = list(parsers.keys())
    key_chose = get_closest_headers(df,parse_keys)
    for key,value in key_chose.items():
        if value == header:
            pattern = parsers.get(key)
            if pattern:
                return list(set(extract_emails(query, pattern)))
    numbers = False
    if header in ["Record ID","Date Pulled",'Combined HELOC & Mortgage Balanced',"MTG10","distance"]:
        numbers=True

    if numbers:
        char_list = ['']
        for char in str(query):
            if char not in list('0123456789-.'):
                char_list[-1]=replace_list(['-','.'],char_list[-1])
                if char_list[-1] != '':
                    char_list.append('')
            else:
                char_list[-1]+=char
                
        return char_list
    for each in list('qwertyuiopasdfghjklzxcvbnm'):
        query = query.replace(f'\{each}','')
    query = query.strip().split(' ')
    for each in ['',' ']:
        while each in query:
            query.remove(each)
    return query
parsed_row = choose_parser('Combined HELOC & Mortgage Balance',"/home/gamook/Desktop/distance/ALL Time Data for Solar.xlsx","""this is the fiinal one
John Putkey
​Arianne Bueta;​
Matthew Matsuda​
​
Brandon Haefele​
here is all the data with distance attributed to zip code, and the original excel with with distance from sac attributed to every row

zips_within sac
[95220, 94501, 94502, 94507, 94706, 94707, 95701, 95221, 95002, 95601, 94503, 95222, 94508, 95843, 94509, 94531, 95703, 95912, 95223, 95913, 94027, 95301, 95603, 95602, 95604, 95224, 95303, 95914, 94565, 95903, 94002, 94920, 95005, 94510, 94705, 94710, 94709, 94708, 94704, 94702, 94703, 94511, 95305, 95917, 94923, 94924, 95006, 95416, 94513, 94553, 94005, 95007, 95606, 95918, 95919, 94010, 94011, 95225, 94514, 94515, 95682, 95709, 95419, 95008, 95011, 95922, 94516, 95010, 95608, 95609, 94546, 94552]


zips_outside of 100 miles drive from sac
[93510, 49301, 97330, 37010, 38310, 49220, 92301, 96006, 42120, 49221, 97901, 37616, 80101, 97406, 91301, 91376, 91390, 92536, 93601, 80720, 32615, 38001, 81101, 97321, 97322, 18210, 18011, 37701, 19018, 95511, 37012, 41001, 32420, 91803, 91801, 91802, 92656, 38504, 80510, 18109, 18104, 18103, 18106, 38541, 80420, 42020, 81210, 93201, 49707, 91901, 91903, 96146, 97324, 91001, 91003, 37301, 32701, 32714, 32716, 32421, 49302, 32702, 16601, 16602, 33920, 97409, 42122, 19002, 97101, 83406, 83401, 59711, 92805, 92804, 92807, 92802, 92806, 92808, 92801, 92817, 92815, 92809, 92812, 92816, 92825, 92803, 96007, 37705, 92305, 48103, 48104, 48105, 48108, 34216, 95412, 17003, 97001, 85086, 32617, 37013, 37011, 81120, 92539, 85120, 85119, 32329, 32320, 37302, 33572, 32712, 32703, 32704, 92308, 92307, 95003, 95001, 91007, 91006, 34266, 34269, 91077, 34265, 95521, 95518, 97102, 18403, 32618, 38449, 19003, 85601, 85123, 59821, 91331, 38002, 97812, 81021, 48005, 95004, 80804, 37014, 93421, 93420, 90701, 90702, 80004, 80003, 80002, 80007, 80005, 80001, 80403, 80006, 93203, 97520, 41102, 37015, 83420, 81611, 81612, 17304, 34705, 19014, 32102, 97103, 93422, 93423, 97813, 37303, 18810, 83801, 32233, 49905, 38004, 38220, 93602, 48326, 33823, 37016, 80610, 97325, 80014, 80018, 80013, 80010, 80016, 80015, 80017, 80012, 97002, 80011, 80019, 80247, 80047, 80046, 80044, 80041, 80040, 80045, 81410, 90704, 34142, 93204, 33160, 33180, 93424, 81620, 33825, 33826, 85323, 19311, 85392, 81022, 97410, 91702, 33827, 82321, 80421, 17502, 32531, 97814, 93307, 93311, 93306, 93313, 93312, 93309, 93314, 93308, 93305, 93301, 93303, 93304, 93389, 93384, 93390, 93380, 93383, 93386, 93302, 93387, 33154, 19004, 91706, 97411, 18013, 97106, 92220, 82601, 40004, 42024, 92311, 92312, 38135, 38133, 38134, 33830, 33831, 81621, 32423, 82410, 93604, 38311, 49015, 38544, 97107, 48706, 81122, 95524, 37708, 97621, 92223, 97108, 15009, 97004, 97007, 97006, 97008, 97005, 97075, 48612, 96129, 40006, 15522, 38313, 37018, 48809, 37019, 59714, 90201, 32619, 37020, 91307, 34756, 96008, 33430, 32809, 32812, 33756, 33786, 33770, 86015, 34420, 34421, 83313, 90706, 90707, 38006, 80512, 37306, 97701, 97702, 97707, 97708, 97709, 80102, 19020, 85602, 37307, 42025, 49022, 40403, 92203, 49103, 80513, 15102, 38315, 18017, 18020, 18015, 37022, 80805, 49617, 81023, 34465, 90212, 90210, 90209, 90211, 48025, 90213, 34464, 92314, 92315, 93605, 82833, 93513, 33043, 49307, 92242, 37023, 38221, 59011, 59911, 59101, 59102, 59106, 59105, 93606, 37308, 19508, 48009, 33161, 93514, 93515, 97412, 80422, 83221, 37709, 96103, 18610, 81123, 19510, 97326, 48301, 48304, 48302, 92316, 38545, 32424, 37617, 19422, 92317, 95525, 97413, 37618, 97622, 92225, 92226, 97818, 33921, 33496, 33498, 33487, 33433, 33432, 33434, 33486, 33431, 33428, 33488, 33497, 33481, 17007, 83716, 83704, 83702, 83709, 83706, 83714, 83713, 83705, 83703, 33922, 38008, 37025, 97623, 81024, 32425, 91902, 91908, 34135, 34134, 34136, 34133, 92003, 81025, 95415, 97009, 93516, 92004, 80303, 80305, 80302, 80301, 80304, 80308, 80307, 80306, 91905, 42104, 42101, 42103, 33834, 33472, 33473, 33435, 33436, 33437, 33426, 33474, 33425, 59718, 59715, 91008, 34212, 34203, 34211, 34202, 34205, 34207, 34208, 34209, 34201, 34210, 34281, 34280, 34204, 34206, 34282, 34217, 38316, 93426, 37026, 40108, 33511, 33510, 33509, 33508, 32008, 48614, 92227, 92821, 92823, 92822, 80424, 37027, 37024, 93517, 15017, 80611, 80602, 80601, 38011, 80603, 48114, 80640, 48116, 97011, 19007, 37620, 37621, 32321, 48097, 32621, 32622, 19015, 97415, 49230, 34614, 34604, 34602, 34605, 34613, 34601, 19008, 80023, 80021, 80020, 80038, 97712, 48416, 38012, 97327, 42210, 15417, 38317, 80723, 38547, 32009, 19010, 38222, 85396, 85326, 40010, 93427, 90620, 90621, 90622, 81211, 38318, 82834, 38548, 86429, 86442, 37711, 37028, 32110, 91506, 91504, 91505, 91501, 91502, 91510, 91503, 83318, 49029, 80807, 41005, 38015, 96013, 37029, 97720, 18324, 33513, 37640, 59750, 93206, 97109, 37713, 80103, 38549, 92230, 49601, 81320, 91302, 91372, 83607, 83605, 49316, 92231, 92232, 80808, 37309, 93518, 41007, 93505, 93504, 92320, 92233, 32011, 96014, 95418, 96124, 93010, 93012, 93011, 97416, 93428, 38320, 17011, 97730, 86322, 42718, 91906, 97013, 96015, 32111, 42721, 97110, 91304, 91303, 91305, 81212, 81215, 15317, 48187, 48188, 32533, 93608, 97820, 91351, 91387, 91386, 92587, 97417, 32920, 33914, 33990, 33904, 33991, 33909, 33993, 33915, 33910, 92624, 81623, 18407, 92007, 85377, 48117, 17015, 17013, 95528, 92009, 92010, 92008, 92018, 92013, 92011, 97111, 93923, 93922, 93921, 93924, 96140, 93013, 93014, 80612, 32322, 90746, 90745, 90749, 37030, 93609, 37714, 32427, 85122, 85193, 80809, 97014, 48064, 82609, 82604, 96016, 32707, 32718, 49031, 91384, 91310, 37031, 80108, 80104, 80109]





John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361



Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you


TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions
Arianne Bueta
​Matthew Matsuda;​
John Putkey​
​
Brandon Haefele​

This is just 2023 not 2022.

From: Matthew Matsuda <Matt@westlakeoc.com>
Sent: Friday, April 19, 2024 12:25 PM
To: John Putkey <jputkey@westlakeoc.com>; Arianne Bueta <arianne@westlakeoc.com>
Cc: Brandon Haefele <brandon@westlakeoc.com>
Subject: RE: this is the fiinal one

 

Arianne,

 

This excel that’s provided is less than 6k records. Just so we are all on thee same page, this data is from the last two years correct?

 

From: John Putkey <jputkey@westlakeoc.com>
Sent: Friday, April 19, 2024 11:41 AM
To: Matthew Matsuda <Matt@westlakeoc.com>; Arianne Bueta <arianne@westlakeoc.com>
Subject: Re: this is the fiinal one

 

there is the full scrub. the following are the zips that were out of range

91901

91903

96146

91506

91504

91505

91501

91502

91510

91503

 96140

 



John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions

From: John Putkey <jputkey@westlakeoc.com>
Sent: Friday, April 19, 2024 12:47 PM
To: Matthew Matsuda <Matt@westlakeoc.com>
Subject: Fw: this is the fiinal one

 

 

 



John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions

From: John Putkey <jputkey@westlakeoc.com>
Sent: Friday, April 19, 2024 12:47 PM
To: Arianne Bueta <arianne@westlakeoc.com>
Subject: Re: this is the fiinal one

 

ahh, its different on my end, probably has to do with browser. will get with you after this to make sure its good on your end

 



John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions

From: Arianne Bueta <arianne@westlakeoc.com>
Sent: Friday, April 19, 2024 12:43 PM
To: John Putkey <jputkey@westlakeoc.com>
Cc: Matthew Matsuda <Matt@westlakeoc.com>
Subject: RE: this is the fiinal one

 

Is this, okay? Like, the column header is not working

 

 

From: John Putkey <jputkey@westlakeoc.com>
Sent: Friday, April 19, 2024 10:41 AM
To: Arianne Bueta <arianne@westlakeoc.com>
Cc: Matthew Matsuda <Matt@westlakeoc.com>
Subject: Re: this is the fiinal one

 

https://45.55.134.98:5050/

its parsing, give it a shot. im runing the distance data rn

 



John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions

From: John Putkey <jputkey@westlakeoc.com>
Sent: Friday, April 19, 2024 12:31 PM
To: Arianne Bueta <arianne@westlakeoc.com>
Cc: Matthew Matsuda <Matt@westlakeoc.com>
Subject: Re: this is the fiinal one

 

ahh, yeah, i was doing some updates to the server all together, its been up and down today.

ill do that on my end rn. so far as the distance, ill take a  couple samples of addresses per zip code, and determine it pretty quick by that. ill have it out in a short bit

 



John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions

From: Arianne Bueta <arianne@westlakeoc.com>
Sent: Friday, April 19, 2024 12:28 PM
To: John Putkey <jputkey@westlakeoc.com>
Cc: Matthew Matsuda <Matt@westlakeoc.com>
Subject: RE: this is the fiinal one

 

I was trying again to parse it out to your given link, seems there’s an error with drop-down. I cannot drop it down.

 

This Files has been uploaded on Tuesday and explained it to both Matt & Brandon, and Brandon still wants me to re-check the All data for 2023, that’s why I needed to do a manual filtering.

 

Right now, from what I’ve checked from the file that I’ve gave to you before, I found 10K+ more for specific Zip Codes requested compared to this file which is 6K plus.

 

I’ll send it over for your comparison.

 

Just to confirm, which is more accurate on zip codes, the one you’ve sent it right now with 70 zips? Or the one that Brandon sent to me on Wednesday?(see snip). Yours are way lesser than what I’ve followed actually

 

From: John Putkey <jputkey@westlakeoc.com>
Sent: Friday, April 19, 2024 10:17 AM
To: Arianne Bueta <arianne@westlakeoc.com>
Cc: Matthew Matsuda <Matt@westlakeoc.com>
Subject: this is the fiinal one

 

 

Arianne let me know if we are looking at different excels.
the following are the only zip codes in the data:

[95303, 95305, 90704, 95843, 95903, 95912, 95913, 95914, 95917, 95918, 95919, 95922, 95416, 95419, 94920, 94923, 94924, 91901, 91903, 95002, 95006, 95007, 95010, 94501, 94502, 94503, 94507, 94508, 94509, 94510, 94511, 94513, 94002, 94514, 94515, 94005, 94516, 94010, 94011, 94531, 94027, 94546, 94552, 94553, 94565, 91501, 91502, 91503, 91504, 91505, 91506, 95601, 95603, 95602, 91510, 95604, 95608, 95609, 95606, 96140, 96146, 95682, 95701, 95703, 95709, 94702, 94703, 94704, 94705, 94706, 94707, 94708, 95221, 95222, 95223, 95224, 95225, 94710, 94709]

John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions
Arianne Bueta
​Matthew Matsuda;​
John Putkey​
​
Brandon Haefele​

I can’t go back 2021, instead, I can do 2022. I haven’t got the file that Joanne has from Jan2021 until October 2021 since I don’t have her storage email.
Matthew Matsuda
​John Putkey;​
Arianne Bueta​
​
Brandon Haefele​

Ok I spoke with Brandon though and  this won’t work- Arianne will you please go back THREE years now that we have the for sure correct zip codes please
John Putkey
​Matthew Matsuda;​
Arianne Bueta​
​
Brandon Haefele​

matt,

      originally ~42k rows


      chopped down to 6.5k 2 weeks ago

      and today finalized the ~9 hundered were stickened today from the zips. Here in a few_minutes ill send the              zip codes, their distance from sac and the counts per zip found in the files. For further verify.

 



John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions
Matthew Matsuda
​John Putkey;​
Arianne Bueta​
​
Brandon Haefele​

Arianne,

 

This excel that’s provided is less than 6k records. Just so we are all on thee same page, this data is from the last two years correct?
John Putkey
​Matthew Matsuda;​
Arianne Bueta​

there is the full scrub. the following are the zips that were out of range

91901

91903

96146

91506

91504

91505

91501

91502

91510

91503

 96140

 



John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions
John Putkey
​
Matthew Matsuda​

John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions

You forwarded this message on Fri 2024-04-19 12:47 PM
You forwarded this message on Fri 2024-04-19 12:47 PM
John Putkey
​
Arianne Bueta​

ahh, its different on my end, probably has to do with browser. will get with you after this to make sure its good on your end

 



John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions
Arianne Bueta
​
John Putkey​
​
Matthew Matsuda​

Is this, okay? Like, the column header is not working

 

John Putkey
​
Arianne Bueta​
​
Matthew Matsuda​

https://45.55.134.98:5050/

its parsing, give it a shot. im runing the distance data rn

 



John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions
John Putkey
​
Arianne Bueta​
​
Matthew Matsuda​

ahh, yeah, i was doing some updates to the server all together, its been up and down today.

ill do that on my end rn. so far as the distance, ill take a  couple samples of addresses per zip code, and determine it pretty quick by that. ill have it out in a short bit

 



John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions
Arianne Bueta
​
John Putkey​
​
Matthew Matsuda​

I was trying again to parse it out to your given link, seems there’s an error with drop-down. I cannot drop it down.

 

This Files has been uploaded on Tuesday and explained it to both Matt & Brandon, and Brandon still wants me to re-check the All data for 2023, that’s why I needed to do a manual filtering.

 

Right now, from what I’ve checked from the file that I’ve gave to you before, I found 10K+ more for specific Zip Codes requested compared to this file which is 6K plus.

 

I’ll send it over for your comparison.

 

Just to confirm, which is more accurate on zip codes, the one you’ve sent it right now with 70 zips? Or the one that Brandon sent to me on Wednesday?(see snip). Yours are way lesser than what I’ve followed actually

John Putkey
​
Arianne Bueta​
​
Matthew Matsuda​
of the few ive run, as per google they are 101 and 115 miles, however, google maps from city goes from city center, where we decided to base the distance calcs on is the city limits. with any zips in sac considered 0




John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361



Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you


TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions
John Putkey
​
Arianne Bueta​
​
Matthew Matsuda​

Arianne let me know if we are looking at different excels.
the following are the only zip codes in the data:

[95303, 95305, 90704, 95843, 95903, 95912, 95913, 95914, 95917, 95918, 95919, 95922, 95416, 95419, 94920, 94923, 94924, 91901, 91903, 95002, 95006, 95007, 95010, 94501, 94502, 94503, 94507, 94508, 94509, 94510, 94511, 94513, 94002, 94514, 94515, 94005, 94516, 94010, 94011, 94531, 94027, 94546, 94552, 94553, 94565, 91501, 91502, 91503, 91504, 91505, 91506, 95601, 95603, 95602, 91510, 95604, 95608, 95609, 95606, 96140, 96146, 95682, 95701, 95703, 95709, 94702, 94703, 94704, 94705, 94706, 94707, 94708, 95221, 95222, 95223, 95224, 95225, 94710, 94709]

John Putkey,
(346) 347-9979

 

2945 Townsgate Road, Suite 200

Westlake Village, CA 91361

 


Confidentiality Notice - This e-mail transmission, and any documents, files or previous e-mail messages attached to it, may contain information that is confidential or legally privileged. If you are not the intended recipient, or a person responsible for delivering it to the intended recipient, you are hereby notified that you must not read or play this transmission and that any disclosure, copying, printing, distribution or use of any of the information contained in or attached to this transmission is Strictly Prohibited. If you have received this transmission in error, please immediately notify the sender by telephone or return e-mail and delete the original transmission and its attachments without reading or saving in any manner. Thank you

 

TERMS & CONDITIONS

https://www.westlakeoriginationcenter.com/terms-and-conditions
""")
input(parsed_row)
