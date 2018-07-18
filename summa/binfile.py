objects = []
with (open("/glade/u/home/manab/fcast/SUMMA_ASMO.bin", "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break

