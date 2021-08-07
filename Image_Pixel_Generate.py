import numpy as np
import math
import argparse
import os
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import copy
import random


image_size = 64*100
rows, cols = (64,100)
image_name ='testImg_64x100_eDRAM.png'


def img2bin(row,col,name):
    convertedImg = np.zeros((row, col))
    #open image (binary image) from https://www.pixilart.com/draw?ref=home-page
    binImg = Image.open(name)
    binImg = np.array(binImg)

    # Convert binary image rgba code [0 0 0 255] or [0 0 0 0] to 1 and -1 (memeory array)
    for r in range(row):
        for c in range(col):
            if binImg[r][c][3] > 0.5:
                convertedImg[r][c] = 1
            else:
                convertedImg[r][c] = -1
    return convertedImg


def random_spin_generator(seed,row,col):
    # Randonly create spin (-1 and 1)
    convertedArr = np.zeros((row, col))
    np.random.seed(seed)
    convertedArr = np.floor(np.random.random((row, col)) + .5)

    for r in range(rows):
        for c in range(cols):
            if convertedArr[r][c] > 0.5:
                convertedArr[r][c] = 1
            else:
                convertedArr[r][c] = -1
    return convertedArr


def ind2str(x,y):
    return str(x) + ',' + str(y)


def img2dict_generate_j(rows,cols,image_name):
    target_img = img2bin(rows,cols,image_name)
    padded_target_img = pad_zeros_2_list(target_img,rows,cols)
    # print(padded_target_img)

    # r = 2 # row
    # c = 2 # col
    new_J =[0,0,0,0,0,0,0,0]
    new_J_dict = {}
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            if padded_target_img[r][c] == padded_target_img[r-1][c-1]:
                new_J[0] = 1
            else:
                new_J[0] = -1
            if padded_target_img[r][c] == padded_target_img[r-1][c]:
                new_J[1] = 1
            else:
                new_J[1] = -1
            if padded_target_img[r][c] == padded_target_img[r-1][c+1]:
                new_J[2] = 1
            else:
                new_J[2] = -1
            if padded_target_img[r][c] == padded_target_img[r][c+1]:
                new_J[3] = 1
            else:
                new_J[3] = -1
            if padded_target_img[r][c] == padded_target_img[r+1][c + 1]:
                new_J[4] = 1
            else:
                new_J[4] = -1
            if padded_target_img[r][c] == padded_target_img[r+1][c]:
                new_J[5] = 1
            else:
                new_J[5] = -1
            if padded_target_img[r][c] == padded_target_img[r+1][c-1]:
                new_J[6] = 1
            else:
                new_J[6] = -1
            if padded_target_img[r][c] == padded_target_img[r][c-1]:
                new_J[7] = 1
            else:
                new_J[7] = -1
            new_J_dict[ind2str(r-1, c-1)] = new_J
            new_J = [0, 0, 0, 0, 0, 0, 0, 0]
    return new_J_dict


def H_sigma_cal(r,c,spin,J):
    result = -(spin[r-1,c-1] * J.get(ind2str(r-1,c-1))[0] \
             + spin[r-1,c] * J.get(ind2str(r-1,c-1))[1] \
             + spin[r-1,c+1] * J.get(ind2str(r-1,c-1))[2] \
             + spin[r,c+1] * J.get(ind2str(r-1,c-1))[3] \
             + spin[r+1,c+1] * J.get(ind2str(r-1,c-1))[4] \
             + spin[r+1,c] * J.get(ind2str(r-1,c-1))[5] \
             + spin[r+1,c-1] * J.get(ind2str(r-1,c-1))[6] \
             + spin[r,c-1] * J.get(ind2str(r-1,c-1))[7])
    # print(str(spin[r-1,c-1]) + ',' + str(spin[r-1,c]) + ',' + str(spin[r-1,c+1]) + ',' + str(spin[r,c+1])
    #       + ',' + str(spin[r+1,c+1]) + ',' + str(spin[r+1,c]) + ',' + str(spin[r+1,c-1]) + ',' + str(spin[r,c-1]))

    return result


def update_spin(H_sigma):
    if H_sigma >= 0:
        sigma = -1
    else:
        sigma = 1
    return sigma


def pad_zeros_2_list(thisArray,r,c):
    padded_array = np.zeros((r+2,c+2))-1
    padded_array[1:thisArray.shape[0]+1, 1:thisArray.shape[1]+1] = thisArray
    return padded_array


def Ising_start(this_spin,J,rows,cols,total_iteration,Ising_KPI):
    H_sigma_array = []
    for i in range(total_iteration):
        Ising_energy = 0
        # print('iteration = ' + str(i))
        next_spin = copy.deepcopy(this_spin)
        # print(thisSpinArray)
        for r in range(1,rows+1):
            H_sigma_row = []
            for c in range(1,cols+1):
                # print('(' + str(r-1) + ',' + str(c-1) + ')')
                H_sigma = H_sigma_cal(r, c, this_spin, J)
                H_sigma_row.append(H_sigma)
                Ising_energy = H_sigma*this_spin[r][c] + Ising_energy
                # print('Ising_energy = ' + str(Ising_energy))
                # print('H_sigma = ' + str(H_sigma))
                this_sigma = update_spin(H_sigma)
                # print('this_sigma = ' + str(this_sigma))
                next_spin[r][c] = this_sigma
            H_sigma_array.append(H_sigma_row)
        # print("-------------")
        # for i in range(len(H_sigma_array[0])):
        #     print(H_sigma_array[i])
        H_sigma_array = []
        # H_sigma_array.clear()
        # if i == 2:
        #     plt.imshow(next_spin, cmap='Greys_r')
        #     plt.axis('off')
        #     plt.savefig('Iter2.png')
        #     plt.show()

        # print('next_spin')
        # print(next_spin)
        # print('Ising_energy = ' + str(Ising_energy))
        Ising_KPI.append(Ising_energy)
        this_spin = next_spin

    return next_spin,Ising_KPI,H_sigma_array


def annealing(this_spin,rows,cols):
    howmanyTrue = 0
    for r in range(1, rows + 1):
        for c in range(1, cols + 1):
            np.random.seed(1)
            do_flip = bool(random.getrandbits(1))
            # print(bool(random.getrandbits(1)))
            # print(str(r) + ',' + str(c))
            if do_flip:
                # print('T')
                howmanyTrue = howmanyTrue+1
                # flip the spin randomly
                if this_spin[r][c] == 1:
                    this_spin[r][c] = -1
                else:
                    this_spin[r][c] = 1
            else:
                # print('F')
                this_spin[r][c] = this_spin[r][c]
    return this_spin,howmanyTrue


def annealing_ver2(seed, number_of_flip, this_spin, img_size, col):
    random.seed(seed)

    # generate random number 1 4 6, each number representing flip position
    this_random = random.sample(range(img_size), number_of_flip)

    for i in range(number_of_flip):
        # this_random = random.randint(0,99)
        # print(this_random[i])

        # generate column and row from the random decimal number
        this_c = int(this_random[i] % col)
        this_r = int(math.floor(this_random[i] / col))
        # print("xxxxxxx")
        # print(this_random[i])
        # print(this_r)
        # print(this_c)
        # flip the spin
        if this_spin[this_r+1][this_c+1] == 1:
            this_spin[this_r+1][this_c+1] = -1
        else:
            this_spin[this_r+1][this_c+1] = 1
    return this_spin


def annealing_ver3(image_size,this_spin):
    this_random = np.random.choice([0, 1], size=image_size, p=[.1, .9])
    # print(this_random)
    for i in range(image_size):
        this_c = int(i % math.sqrt(image_size))
        this_r = int(math.floor(i / math.sqrt(image_size)))
        # print("i = " + str(i) + "---- (" + str(this_r) + "," + str(this_c) + ")")

        if this_random[i] == 1:
            if this_spin[this_r+1][this_c+1] == 1:
                this_spin[this_r+1][this_c+1] = -1
            else:
                this_spin[this_r+1][this_c+1] = 1
        else:
            this_spin[this_r + 1][this_c + 1] = this_spin[this_r+1][this_c+1]
    return this_spin


J_dict = {ind2str(2,0): [1,1,-1,-1,1,1,1,1],
          ind2str(2,1): [-1,1,1,1,-1,-1,-1,-1],
          ind2str(2,2): [1,1,-1,-1,-1,-1,-1,1],
          ind2str(2,3): [-1,1,1,1,1,1,1,-1],
          ind2str(0,0): [1,1,1,1,-1,1,1,1],
          ind2str(0,1): [1,1,1,1,-1,-1,1,1],
          ind2str(0,2): [1,1,1,1,1,-1,-1,1],
          ind2str(0,3): [1,1,1,1,1,1,-1,1],
          ind2str(1,0): [1,1,1,-1,-1,1,1,1],
          ind2str(1,1): [-1,-1,-1,1,1,1,-1,-1],
          ind2str(1,2): [-1,-1,-1,-1,-1,1,1,1],
          ind2str(1,3): [1,1,1,1,1,1,-1,-1],
          ind2str(3,0): [1,1,-1,1,1,1,1,1],
          ind2str(3,1): [1,-1,-1,1,1,1,1,1],
          ind2str(3,2): [-1,-1,1,1,1,1,1,1],
          ind2str(3,3): [-1,1,1,1,1,1,1,1]}

Ising_KPI = []
# Generate random spin
randomSpin = random_spin_generator(100,rows,cols)
# print(randomSpin)
initial_spin = pad_zeros_2_list(randomSpin,rows,cols)
# print(initial_spin)

plt.imshow(initial_spin, cmap='Greys_r')
# plt.axis('off')
# plt.savefig('Init.png')
plt.show()


# Generate J
J = img2dict_generate_j(rows,cols,image_name)
# print("JJJJJJ")
# print(J)
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(initial_spin,J,rows,cols,2,Ising_KPI)
# plt.axis('off')
# plt.imshow(this_spin, cmap='Greys_r')
# plt.show()

# annealing
next_spin = annealing_ver2(30,1500,this_spin,image_size, cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()

# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,2,Ising_KPI)
# print(this_spin)
# plt.axis('off')
# plt.imshow(this_spin, cmap='Greys_r')
# plt.show()

# annealing
next_spin = annealing_ver2(20,1300,this_spin,image_size,cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,1,Ising_KPI)
# print(this_spin)
# plt.axis('off')
# plt.imshow(this_spin, cmap='Greys_r')
# plt.show()

# annealing
next_spin = annealing_ver2(3,20,this_spin,image_size,cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,2,Ising_KPI)
# print(this_spin)
# plt.axis('off')
# plt.imshow(this_spin, cmap='Greys_r')
# plt.show()

# annealing
next_spin = annealing_ver2(4,600,this_spin,image_size,cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,1,Ising_KPI)
# print(this_spin)
# plt.axis('off')
# plt.imshow(this_spin, cmap='Greys_r')
# plt.show()

# annealing
next_spin = annealing_ver2(42,30,this_spin,image_size,cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,2,Ising_KPI)
# print(this_spin)
# plt.axis('off')
# plt.imshow(this_spin, cmap='Greys_r')
# plt.show()

# annealing
next_spin = annealing_ver2(6,400,this_spin,image_size,cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,3,Ising_KPI)
# print(this_spin)
# plt.axis('off')
plt.imshow(this_spin, cmap='Greys_r')
plt.show()

# annealing
next_spin = annealing_ver2(63,200,this_spin,image_size,cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,2,Ising_KPI)
# print(this_spin)
# plt.axis('off')
# plt.imshow(this_spin, cmap='Greys_r')
# plt.show()

# annealing
next_spin = annealing_ver2(35,100,this_spin,image_size,cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,5,Ising_KPI)
# print(this_spin)
# plt.axis('off')
# plt.imshow(this_spin, cmap='Greys_r')
# plt.show()

# annealing
next_spin = annealing_ver2(95,50,this_spin,image_size,cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,1,Ising_KPI)
# print(this_spin)
# plt.axis('off')
# plt.imshow(this_spin, cmap='Greys_r')
# plt.show()

# annealing
next_spin = annealing_ver2(75,30,this_spin,image_size,cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,2,Ising_KPI)
# print(this_spin)
# plt.axis('off')
# plt.imshow(this_spin, cmap='Greys_r')
# plt.show()

# annealing
next_spin = annealing_ver2(21,10,this_spin,image_size,cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,3,Ising_KPI)
# print(this_spin)
# plt.axis('off')
# plt.imshow(this_spin, cmap='Greys_r')
# plt.show()

# annealing
next_spin = annealing_ver2(22,20,this_spin,image_size,cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,2,Ising_KPI)
# print(this_spin)
# plt.axis('off')
# plt.imshow(this_spin, cmap='Greys_r')
# plt.show()


# annealing
next_spin = annealing_ver2(38,10,this_spin,image_size,cols)
# plt.imshow(next_spin, cmap='Greys_r')
# plt.show()
# start Ising
this_spin,KPI,H_sigma_array = Ising_start(next_spin,J,rows,cols,20,Ising_KPI)
# print(this_spin)
# plt.axis('off')
plt.imshow(this_spin, cmap='Greys_r')
plt.show()



# show KPI
# figure(figsize=(6.5, 8), dpi=80)
plt.plot(KPI,marker='o', color='b', linewidth=2)
plt.xlabel("Spin Iteration",fontsize=16,fontweight='bold')
plt.ylabel('Energy',fontsize=16,fontweight='bold')
# plt.xticks(np.arange(0,21,2),fontsize=16,fontweight='bold')
# plt.yticks(fontsize=16,fontweight='bold')
plt.savefig('energy.png')
plt.show()











