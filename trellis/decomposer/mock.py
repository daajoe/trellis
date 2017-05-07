
#TODO:
def compute_ordering_htd_mock(file_name, ostream, path, iterations=100, seed=0):
    with open('%s/../../LI-encodings/test/Brinkmann-htd.decomp' % path) as f:
        ostream.write('\n'.join(f.readlines()))
