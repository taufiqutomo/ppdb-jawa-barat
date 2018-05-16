'''
Simulasi PPDB
By: Taufiq Akbari Utomo
Created: 21-06-2016
'''
 
import operator
import csv
 
refugee = {}
 
'''
Part 0: Prosedur masukkan siswa ke sekolah, peringkat, lempar yang lain
'''
def bump(entrant, pil1, tahap):
    # masukkan entrant (dict) ke sekolah pilihan 1 (pil1==True) atau pilihan 2
    global diterima
    global refugee
    global lempar
    # tentukan pilihan sekolah
    if pil1:
        pilihan = entrant['Pilihan'][0]
    else:
        pilihan = entrant['Pilihan'][1]
    # masukkan
    kandidat = entrant
    while tahap <= 2:
        diterima[pilihan][tahap].append(kandidat)
        diterima[pilihan][tahap] = sorted(diterima[pilihan][tahap],key=operator.itemgetter('Skor','INA','ENG','MAT','IPA'))
        # kalau kuota berlebih, lempar siswa dengan skor terendah
        if len(diterima[pilihan][tahap]) > kuota[pilihan][tahap]:
            kandidat = diterima[pilihan][tahap][0]
            del diterima[pilihan][tahap][0]
            # Lempar dari DW ke GW, dari GW ke LK
            tahap = tahap+1
        else:
            break
    refugee = kandidat
    if tahap == 3 and pilihan == refugee['Pilihan'][0] and len(refugee['Pilihan']) == 2:
        # refugee terlempar dari pilihan 1, lempar ke pilihan 2
        lempar = True
 
'''
Part 1: Data kuota dan data pendaftar
'''
# data kuota
f = open('Kuota simulasi.csv', 'r', newline = '')
list_kuota = csv.reader(f)
kuota = []
for row in list_kuota:
    for i in range(len(row)):
        row[i] = eval(row[i])
    kuota.append(row)
f.close()
# data pendaftar
f = open('data simulasi.csv', 'r+', newline = '')
reader = csv.DictReader(f)
pendaftar = []
for row in reader:
    p1 = row['Pilihan 1']
    p2 = row['Pilihan 2']
    matpil = '['+p1+','+p2+']' # ada solusi yang lebih baik?
    row['Pilihan'] = eval(matpil)
    row['Skor'] = eval(row['Skor'])
    row['Tahap P1'] = eval(row['Tahap P1'])
    row['Tahap P2'] = eval(row['Tahap P2'])
    pendaftar.append(row)
f.close()
 
'''
Part 2: Data siswa diterima
'''
diterima = []
for i in range(len(kuota)):
    diterima.append([[],[],[]])
 
'''
Part 3: Seleksi
'''
for student in pendaftar:
    lempar = False
    bump(student, True, student['Tahap P1'])
    while lempar:
        lempar = False
        bump(refugee, False, refugee['Tahap P2'])
 
'''
Part 4: Output passing grade
'''
PG = []
for default in range(len(kuota)):
    PG.append([0,0,0])
for count in range(len(diterima)):
    PG_sekolah = [0,0,0]
    for i in range(3):
        '''
       print("==")
       for siswa in hasil[i]:
           print(siswa['Nama'], siswa['Skor'])
       '''
        if len(diterima[count][i]) > 0:
            PG_sekolah[i] = diterima[count][i][0]['Skor']
    PG_sekolah[1] = min(PG_sekolah[1:])
    PG[count] = PG_sekolah
 
rekap = []
for i in range(1,len(PG)):
    to_add = {}
    sekolahan = "SMAN "+str(i)
    to_add["Sekolah"] = sekolahan
    to_add["PG Tahap 1"] = PG[i][0]
    to_add["PG Tahap 2"] = PG[i][1]
    to_add["PG Luar Kota"] = PG[i][2]
    rekap.append(to_add)
 
field = ["Sekolah", "PG Tahap 1", "PG Tahap 2", "PG Luar Kota"]
g = open('rekapitulasi simulasi.csv', 'w', newline = '')
writer = csv.DictWriter(g, fieldnames = field)
writer.writeheader()
for rekap_sekolah in rekap:
    writer.writerow(rekap_sekolah)
g.close()