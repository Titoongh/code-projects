import pandas as pd
data = open('names/nam_dict.txt','r')

line_count = 0
country_dic = {}
country = None
country_idx = None
df = pd.DataFrame(columns=['name','frequence'])
cpt = 0


for line in data:
    line_count += 1
    if 178 <= line_count <= 287 :
        if country == None:
            for l in line.split(' ')[1:]:
                if l != '' :
                    country = l
                    break
        else :
            try :
                country_dic[country] = line.split(' ').index('|') + 1
                country = None
            except :
                continue

    if line_count >= 305 :
        FR_idx = country_dic['France']
        for i,l in enumerate(line):
            if i == FR_idx and l != ' ':
                df.loc[cpt,'name'] = line.split()[1]
                df.loc[cpt,'frequence'] = l
                cpt += 1

print df
df.to_csv('name_list.csv')
