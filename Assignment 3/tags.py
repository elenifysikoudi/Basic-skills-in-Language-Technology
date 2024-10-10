def HMM():
    file = 'tags.toks_tags'
    with open (file, 'r') as tags:
        for sentence in tags:
            print(sentence)

if __name__ == "__main__":
    HMM()
