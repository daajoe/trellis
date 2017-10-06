from trellis.decomposer.pace import PACEDecomposer


# TODO: Jdrasil heuristic
# -heuristic

class Jdrasilv1(PACEDecomposer):
    name = 'jdrasil2016'
    bin_name = 'jdrasil'
    folder_name = 'jdrasil2016'

    args = ['-log -e PBLib_incremental', '-log -e commander', '-log -e PBLib']