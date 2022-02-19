import re

snowman = {True:
    (
        "do you want to build a snowman",
        "do you want to build a snowman?",
    )

}

tmp = "do you want to build a jenny snoWman?"
re.search("^do you want to build|code a\s?\w*\s*snowman\??$", tmp)

for item in snowman:
    for sample in snowman[item]:
        if re.search("^do you want to build|code a\s?\w*\s*snowman\??$", sample):
            pass
        else:
            print(sample)