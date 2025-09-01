import random, colorama 

colorama.init()
while True:
    nums = [random.randint(0, 9), random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),random.randint(0, 9),]
    for i in nums:
        print(f"{colorama.Fore.GREEN}{i}{colorama.Style.RESET_ALL}", end="")
