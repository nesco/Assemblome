file = open('sars_structure.fna')
lines = [line.strip() for line in file]
sars = ''.join(lines)

utr3 = sars[:265]
orf1a = sars[265:13483]
orf1b = sars[13483:21555]
trans12 = sars[21555:21562]
spike = sars[21562:25384]
orf2b = sars[21743:21860]
trans23 = sars[25384:25392]
orf3a = sars[25392:26220]
orf3c = sars[25456:25579]
orf3d = sars[25523:25694]
orf3d2 = sars[25595:25694]
orf3b = sars[25813:26281]
enveloppe = sars[26244:26472]
membrane = sars[26522:27191]
trans56 = sars[27191:27201]
orf6 = sars[27201:27387]
trans67 = sars[27387:27393]
orf7a = sars[27393:27759]
orf7b = sars[27755:27887]
trans78 = sars[27887:27893]
orf8 = sars[27893:28259]
trans89 = sars[28259:28273]
nucleocapsid = sars[28273:29533]
orf9b = sars[28283:28572]
orf9c = sars[28728:28950]
orf10 = sars[29557:29674]
utr5 = sars[29674:]

def write_to_files(sars):
    # Define the segments and their start and end positions in the sars sequence
    segments = {
        'utr3': (0, 265),
        'orf1a': (265, 13483),
        'orf1b': (13483, 21555),
        'trans12': (21555, 21562),
        'spike': (21562, 25384),
        'orf2b': (21743, 21860),
        'trans23': (25384, 25392),
        'orf3a': (25392, 26220),
        'orf3c': (25456, 25579),
        'orf3d': (25523, 25694),
        'orf3d2': (25595, 25694),
        'orf3b': (25813, 26281),
        'enveloppe': (26244, 26472),
        'membrane': (26522, 27191),
        'trans56': (27191, 27201),
        'orf6': (27201, 27387),
        'trans67': (27387, 27393),
        'orf7a': (27393, 27759),
        'orf7b': (27755, 27887),
        'trans78': (27887, 27893),
        'orf8': (27893, 28259),
        'trans89': (28259, 28273),
        'nucleocapsid': (28273, 29533),
        'orf9b': (28283, 28572),
        'orf9c': (28728, 28950),
        'orf10': (29557, 29674),
        'utr5': (29674, len(sars))
    }

    # Loop through each segment, extract the sequence, and write it to a file
    for segment, (start, end) in segments.items():
        filename = f"structure_{segment}.fna"
        with open(filename, 'w') as file:
            file.write(sars[start:end])

# Example usage
# sars = "your_sequence_here"
# write_to_files(sars)
