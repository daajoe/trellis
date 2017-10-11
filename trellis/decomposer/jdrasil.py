from trellis.decomposer.pace import PACEDecomposer


# TODO: Jdrasil heuristic
# -heuristic

class Jdrasilv1(PACEDecomposer):
    name = 'jdrasil'
    bin_name = 'jdrasil'
    folder_name = 'jdrasil'

    args = ['-log -e PBLib_incremental', '-log -e commander', '-log -e PBLib']