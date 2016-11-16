ff = open("test.map", "w+")
import random
type = ["H","H","H","F"]
for i in range(1000):
    geox = str(random.randint(1, 89)) + "." + str(random.randint(0, 10000))
    geoy = str(random.randint(1, 89)) + "." + str(random.randint(0, 10000))
    ele =type[random.randint(0,3)]
    ff.write(geox + ":" + geoy + ":" + ele+ "\n")
ff.close()
