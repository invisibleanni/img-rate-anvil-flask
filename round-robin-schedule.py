import csv
import random
import pandas as pd

# total images
R_IMAGES_TOTAL = 120
F_IMAGES_TOTAL = 480
# R_IMAGES_TOTAL = 20
# F_IMAGES_TOTAL = 80

# need to maintain an 80 20 split of fake v real
R_IMAGES_PER_GROUP = 30
F_IMAGES_PER_GROUP = 120
# R_IMAGES_PER_GROUP = 20
# F_IMAGES_PER_GROUP = 80

PID_TOTAL = 50  # total 50 participants
SESS_PER_PID = 2  # 2 sesisons per participant
RRC_PER_PID = PID_TOTAL * SESS_PER_PID // (R_IMAGES_TOTAL // R_IMAGES_PER_GROUP)


def generate_filenames(prefix, start, end):
    return [f"{prefix}{i}.png" for i in range(start, end + 1)]


csv_header = ["p-id", "sess", "rrc", "img"]
r_images = generate_filenames("r", 1, R_IMAGES_TOTAL)
# we get r1.png, r2.png, r3.png, r4.png, r5.png, r6.png, ... r120.png

f_images = generate_filenames("f", 1, F_IMAGES_TOTAL)
# we get f1.png, f2.png, f3.png, f4.png, f5.png, f6.png, ... f480.png


csv_data = []
rrc = 1  # round-robin-count

for pid in range(1, PID_TOTAL + 1):
    # for each participant starting from 1 to 50 (range (1,50) --> 1,2,3,...50)

    for sess in range(SESS_PER_PID):
        # 1 participant has 2 session, so for each session:

        r_start = ((pid - 1) * SESS_PER_PID + sess) * R_IMAGES_PER_GROUP % R_IMAGES_TOTAL + 1

        # (( (0*2 + 0) * 20 ) % 100) + 1 = 1 -- 20
        # (((0 * 2 + 1) * 20) % 100) + 1 = 21 -- 40
        #
        # (((1 * 2 + 0) * 20) % 100) + 1 = 41 -- 60
        # (((1 * 2 + 1) * 20) % 100) + 1 = 61 -- 80
        # ...

        f_start = ((pid - 1) * SESS_PER_PID + sess) * F_IMAGES_PER_GROUP % F_IMAGES_TOTAL + 1
        # similarly

        r_indx, f_indx = r_start - 1, f_start - 1

        r_subset = r_images[r_indx: (r_indx + R_IMAGES_PER_GROUP)]
        f_subset = f_images[f_indx: (f_indx + F_IMAGES_PER_GROUP)]

        random.shuffle(r_subset)
        random.shuffle(f_subset)

        img_list = r_subset + f_subset

        # shuffle again
        random.shuffle(img_list)

        csv_data.append(
            [f"pid-{pid:02}", f"sess-{sess}", f"rrc-{rrc}", ", ".join(img_list)]
        )

        # Increment rrc every 5 rows (logically according to the diagram on email)
        if len(csv_data) % 5 == 0:
            rrc += 1

# Write the corrected data to a new CSV file
csv_filename = f"./round_robin_LIST_{PID_TOTAL}p_{SESS_PER_PID}s_{F_IMAGES_PER_GROUP}f_{R_IMAGES_PER_GROUP}r_shuffled.csv"
with open(csv_filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(csv_header)
    writer.writerows(csv_data)

# Output produced by the above
# p-id,sess,rrc,img
# pid-01,sess-0,rrc-1,"f12.png, r5.png, f44.png, f55.png, r10.png, f63.png, f54.png, f59.png, f53.png, f39.png, f76.png, r6.png, f30.png, f9.png, f13.png, f79.png, r4.png, f4.png, r3.png, f1.png, f80.png, f49.png, r8.png, f71.png, f31.png, f61.png, f35.png, f38.png, f58.png, r20.png, f19.png, f72.png, f42.png, f62.png, f74.png, r14.png, f52.png, f57.png, f29.png, f41.png, f64.png, f22.png, f70.png, r17.png, f45.png, r11.png, f10.png, r9.png, f51.png, r18.png, f36.png, f40.png, f66.png, f2.png, f23.png, f67.png, f56.png, f47.png, f50.png, f7.png, f43.png, f16.png, f27.png, r12.png, f17.png, f6.png, f28.png, f65.png, f5.png, f37.png, r2.png, r15.png, f26.png, f69.png, f18.png, f60.png, r7.png, r1.png, f78.png, f25.png, f32.png, f15.png, r19.png, f14.png, f68.png, f73.png, f75.png, f77.png, f46.png, f24.png, f8.png, f3.png, f33.png, f34.png, f11.png, f48.png, f20.png, r13.png, f21.png, r16.png"
# pid-01,sess-1,rrc-1,"f100.png, f89.png, f132.png, f139.png, f109.png, r32.png, r40.png, f138.png, r37.png, f156.png, f114.png, f103.png, f108.png, f113.png, f85.png, r24.png, f97.png, f122.png, f102.png, f147.png, f121.png, f159.png, r28.png, f88.png, f91.png, f130.png, f83.png, f101.png, f106.png, f158.png, f133.png, r25.png, f128.png, f155.png, f143.png, r30.png, r23.png, f157.png, f148.png, f140.png, f125.png, f131.png, r27.png, r29.png, f154.png, f137.png, r22.png, f145.png, f118.png, f104.png, f127.png, f116.png, f126.png, f94.png, f93.png, f134.png, f110.png, f135.png, f141.png, f149.png, r33.png, f115.png, r34.png, f146.png, f129.png, f99.png, r21.png, f136.png, f111.png, f150.png, r26.png, f84.png, f160.png, f153.png, f119.png, f82.png, f124.png, r35.png, f142.png, f105.png, f92.png, f144.png, r36.png, r38.png, f112.png, r31.png, f87.png, f98.png, f95.png, f123.png, r39.png, f81.png, f96.png, f86.png, f117.png, f90.png, f107.png, f152.png, f120.png, f151.png"
# pid-02,sess-0,rrc-1,"f172.png, f240.png, f194.png, f220.png, f215.png, f165.png, r56.png, f189.png, f216.png, r53.png, r54.png, r55.png, f237.png, f226.png, f225.png, f177.png, f178.png, r59.png, f195.png, f184.png, f181.png, f232.png, f168.png, f198.png, f205.png, f163.png, r41.png, r43.png, f201.png, f169.png, f186.png, f204.png, f212.png, r58.png, f173.png, f187.png, f214.png, f228.png, f188.png, f174.png, f238.png, f162.png, f230.png, f197.png, f192.png, f231.png, f166.png, f219.png, f199.png, f229.png, f167.png, f224.png, f208.png, f196.png, r57.png, f200.png, r51.png, r52.png, f171.png, f218.png, f170.png, f185.png, r42.png, r50.png, r48.png, f176.png, f203.png, f236.png, f191.png, f164.png, f234.png, f183.png, f202.png, f179.png, f222.png, f213.png, f193.png, f211.png, f221.png, r46.png, f210.png, f209.png, f182.png, f223.png, r45.png, f175.png, f190.png, f227.png, r49.png, r60.png, f217.png, r44.png, f161.png, f207.png, f235.png, f206.png, f239.png, r47.png, f180.png, f233.png"


# now melting....


df = pd.read_csv(csv_filename)
df["img"] = df["img"].str.split(", ")  # Melt the DataFrame on the "img" column, creating a new row for each image
df_exploded = df.explode("img")

df_exploded.reset_index(drop=True, inplace=True)

# csv_filename_melted = "./round_robin__melted_50p_2s_120f_30r_shuffled.csv"
csv_filename_melted = f"./round_robin__melted_{PID_TOTAL}p_{SESS_PER_PID}s_{F_IMAGES_PER_GROUP}f_{R_IMAGES_PER_GROUP}r_Shuffled_Exploded.csv"
df_exploded.to_csv(csv_filename_melted, index=False)
