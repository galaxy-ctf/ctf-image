import random

false_flags = [
    "bad luck, no flag here!",
    "move a long, nothing to see here!",
    "files files everywhere and not a flag to see",
    "Nope.",
    "these are not the flags you are looking for"
    ]

true_flag = 'congrats, you found me! gccctf{finding_flags_fia_ftp_folders_ftw}'

for i in range(0,100):
    if i == 42:
        flag = true_flag
    else:
        flag = false_flags[random.randint(0, len(false_flags)-1)]

    filename = 'flag'+str(i)+'.txt'
    with open(filename, 'w') as f:
        f.write(flag)
